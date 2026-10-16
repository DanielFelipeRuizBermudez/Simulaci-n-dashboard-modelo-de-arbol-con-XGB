# Modelo de mora temprana (Delinquency)

Tarea 4 · Sprint 2 · Predictive Model (Delinquency)
Piloto: Michelle · Copiloto: Daniel · Revisa: Maria
Reporte completo: `streamlit_demo/reports/validation_report_delinquency.json` (generado con `python evaluate_models.py delinquency`)

## Cumplimiento de las subtareas de Trello

| Subtarea de Trello | Cómo se cumple | Dónde |
|---|---|---|
| Select predictor variables (payment history, income, behavior) | 6 variables: historial de pago (`avg_days_late_last_year`, `credit_utilization`), ingreso y exposición (`monthly_income_cop`, `credit_exposure_cop`) y relación con el banco (`num_active_products`, `months_with_bank`) | `DELINQUENCY_FEATURES` en `train_models.py` |
| Train the XGBoost and tune hyperparameters and decision threshold to optimize F2-score | Búsqueda en malla de 24 combinaciones y umbral elegido para maximizar F2 en validación | `train_models.py` |
| Validate the model with historical delinquency data | Evaluación sobre 1.200 clientes históricos de validación (20 % estratificado), con los datos validados por las reglas de la Tarea 2 | `evaluate_models.py` y el reporte JSON |
| Document the results, the most influential variables, and the model's limitations | Este documento | `streamlit_demo/docs/model_delinquency.md` |

## Configuración del modelo

| Parámetro | Valor |
|---|---|
| Variable respuesta | `defaulted_30_60_days` (mora de 30/60 días) |
| Algoritmo | XGBoost (`max_depth` = 3, `learning_rate` = 0,05, `n_estimators` = 150) |
| Desbalance | `scale_pos_weight` = 4,51 (18 % de clientes en mora) |
| Métrica de selección | F2: pesa el recall el doble que la precisión, porque no detectar a un cliente que entra en mora cuesta más que revisar a uno que no |
| Umbral de decisión | 0,332 |

## Resultados en validación (1.200 clientes)

| Métrica | Valor |
|---|---|
| **F2** | **0,538** |
| Recall | 0,931 (detecta 203 de 218 clientes que entraron en mora) |
| Precisión | 0,200 |

Matriz de confusión:

| | Predicho: no mora | Predicho: mora |
|---|---|---|
| **Real: no mora** | 169 | 813 |
| **Real: mora** | 15 | 203 |

## Variables más influyentes (SHAP)

Promedio del valor absoluto de SHAP en el conjunto de validación.

| # | Variable | SHAP medio |
|---|---|---|
| 1 | `monthly_income_cop` | 0,473 |
| 2 | `credit_utilization` | 0,102 |
| 3 | `avg_days_late_last_year` | 0,087 |
| 4 | `credit_exposure_cop` | 0,060 |
| 5 | `months_with_bank` | 0,059 |

El ingreso mensual domina la predicción, seguido por el uso del cupo y el historial de atraso.

## Comparación con las variables derivadas (Tarea 2)

Se entrenó una versión alterna con los mismos hiperparámetros, agregando `debt_to_income_ratio` y `late_over_30_days`, solo para medir su aporte.

| Versión | F2 | Recall | Precisión |
|---|---|---|---|
| Modelo actual (6 variables) | 0,538 | 0,931 | 0,200 |
| Con variables derivadas (8 variables) | 0,536 | 0,927 | 0,199 |

No hay mejora (−0,002 en F2), porque las variables derivadas se calculan a partir de columnas que el modelo ya usa. Se mantiene el modelo actual para no cambiar las entradas de la app; las variables derivadas quedan disponibles para una próxima versión.

## Limitaciones

- **Datos sintéticos.** Las relaciones entre variables fueron generadas por simulación; el desempeño con datos reales de FinBank puede ser distinto.
- **Muchas alertas.** Por priorizar el recall, el modelo marca al 85 % de los clientes de validación (1.016 de 1.200). Antes de producción conviene revisar el umbral con el equipo de cobranza según su capacidad de contacto.
- **Umbral ajustado en el mismo conjunto de validación.** El F2 reportado puede ser algo optimista; lo ideal es confirmarlo en un conjunto de prueba independiente o con validación temporal.
- **Posible sesgo por ingreso.** El ingreso es la variable con más peso; hay que vigilar que el modelo no penalice de forma desproporcionada a los segmentos de menor ingreso.
