# Modelo de fuga de clientes (Churn)

Tarea 5 · Sprint 2 · Predictive Model (Churn)
Piloto: Michelle · Copiloto: Daniel · Revisa: Maria
Reporte completo: `streamlit_demo/reports/validation_report_churn.json` (generado con `python evaluate_models.py churn`)

## Cumplimiento de las subtareas de Trello

| Subtarea de Trello | Cómo se cumple | Dónde |
|---|---|---|
| Select the most relevant variables to predict customer churn | 6 variables de uso de producto, servicio y relación con el banco: `product_usage_score`, `competitor_rate_inquiries`, `complaint_count_last_year`, `active_products_change_6m`, `client_value_score`, `months_with_bank` | `CHURN_FEATURES` en `train_models.py` |
| Train and tune a XGBoost model to maximize the F1-score and predict churn within the next three months | Búsqueda en malla de 24 combinaciones y umbral elegido para maximizar F1 en validación | `train_models.py` |
| Evaluate the model using F1-score on the validation set | Evaluación sobre 1.200 clientes de validación (20 % estratificado), con los datos validados por las reglas de la Tarea 3 | `evaluate_models.py` y el reporte JSON |
| Document the results, the most important variables, and the limitations of the model | Este documento | `streamlit_demo/docs/model_churn.md` |

## Configuración del modelo

| Parámetro | Valor |
|---|---|
| Variable respuesta | `churned_3_months` (fuga en los próximos 3 meses) |
| Algoritmo | XGBoost (`max_depth` = 3, `learning_rate` = 0,05, `n_estimators` = 150) |
| Desbalance | 15 % de clientes con fuga; `scale_pos_weight` = 1 (la búsqueda no mejoró al ponderar) |
| Métrica de selección | F1: equilibrio entre no perder clientes en riesgo y no saturar al equipo comercial |
| Umbral de decisión | 0,153 |

## Resultados en validación (1.200 clientes)

| Métrica | Valor |
|---|---|
| **F1** | **0,296** |
| Recall | 0,576 (detecta 102 de 177 clientes que se fueron) |
| Precisión | 0,199 |

Matriz de confusión:

| | Predicho: se queda | Predicho: se va |
|---|---|---|
| **Real: se queda** | 612 | 411 |
| **Real: se va** | 75 | 102 |

## Variables más influyentes (SHAP)

| # | Variable | SHAP medio |
|---|---|---|
| 1 | `product_usage_score` | 0,210 |
| 2 | `active_products_change_6m` | 0,187 |
| 3 | `competitor_rate_inquiries` | 0,169 |
| 4 | `complaint_count_last_year` | 0,075 |
| 5 | `client_value_score` | 0,059 |

Bajo uso de productos, cierre reciente de productos y consultas de tasas en la competencia son las señales más fuertes de fuga.

## Comparación con las variables derivadas (Tarea 3)

Se entrenó una versión alterna con los mismos hiperparámetros, agregando `complaints_per_month` y `products_declining`, solo para medir su aporte.

| Versión | F1 | Recall | Precisión |
|---|---|---|---|
| Modelo actual (6 variables) | 0,296 | 0,576 | 0,199 |
| Con variables derivadas (8 variables) | 0,293 | 0,559 | 0,199 |

El F1 prácticamente no cambia (−0,002) y el recall baja un poco. Se mantiene el modelo actual.

## Limitaciones

- **F1 bajo (0,30).** De cada 5 clientes marcados, 1 realmente se va. El modelo sirve para priorizar a quién contactar, no para decidir por sí solo.
- **Datos sintéticos.** El ruido de la simulación limita cuánto se puede predecir; con datos reales de FinBank el desempeño puede ser distinto.
- **Umbral ajustado en el mismo conjunto de validación.** El F1 reportado puede ser algo optimista.
- **Dependencia de la versión de XGBoost.** Los modelos deben guardarse y cargarse con la misma versión mayor; por eso conviene fijarla en `requirements.txt`.

## Plan de mejora

- Incorporar variables de comportamiento reciente (transacciones del último mes, contactos al call center).
- Validar con un conjunto de prueba independiente o una partición temporal.
- Fijar la versión de XGBoost y guardar los modelos con `save_model` (formato JSON), que es estable entre versiones.
