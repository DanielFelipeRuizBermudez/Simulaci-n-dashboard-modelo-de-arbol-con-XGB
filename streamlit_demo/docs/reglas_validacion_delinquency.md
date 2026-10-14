# Reglas de validación – datos de mora (Delinquency)

Tarea 2 · Sprint 1 · Data Transformation and Cleaning (Delinquency)
Piloto: Daniel (reglas de negocio) · Copiloto: Maria (las traduce a condiciones verificables)

Estas reglas se aplican en cada carga, antes de entrenar o puntuar el modelo de mora.
Si una regla falla, los datos **no** pasan al modelo.

| # | Regla de negocio | Condición verificable | Columnas |
|---|---|---|---|
| R1 | Toda la información obligatoria debe estar presente | Sin valores nulos | `client_id` y las 6 variables del modelo (+ `defaulted_30_60_days` en el histórico) |
| R2 | Los indicadores tipo score/porcentaje deben ser coherentes | `credit_utilization` en [0, 1] | `credit_utilization` |
| R3 | Montos y conteos no pueden ser negativos (outliers imposibles) | ≥ 0; `avg_days_late_last_year` ≤ 365 | ingresos, exposición, días de mora, productos, antigüedad |
| R4 | Formato correcto | Las variables del modelo son numéricas | las 6 variables del modelo |
| R5 | Un cliente aparece una sola vez por carga | `client_id` sin duplicados | `client_id` |
| R6 | El target es binario | `defaulted_30_60_days` ∈ {0, 1} | `defaulted_30_60_days` (solo histórico) |

## Limpieza previa (transformaciones seguras)

- `client_id` se normaliza: sin espacios y en mayúsculas.
- Se eliminan filas duplicadas exactas (misma información repetida en la carga).

## Variables derivadas del historial de pago

| Variable | Fórmula | Para qué sirve |
|---|---|---|
| `debt_to_income_ratio` | `credit_exposure_cop / monthly_income_cop` | Cuántos meses de ingreso representa la deuda del cliente (capacidad de pago) |
| `late_over_30_days` | 1 si `avg_days_late_last_year` ≥ 30, si no 0 | Marca a quien ya tiene historial de mora de 30 días o más |

Nota: los datos sintéticos no tienen fechas de pago ni valor de cuota, por eso no se calculan
"días desde el último pago" ni "razón pago/cuota". Se usan las equivalentes disponibles.
