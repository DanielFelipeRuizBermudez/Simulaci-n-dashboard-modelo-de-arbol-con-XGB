# Reglas de validación – datos de churn

Tarea 3 · Sprint 1 · Data Transformation and Cleaning (Churn)
Piloto: Daniel (reglas de negocio) · Copiloto: Maria (las traduce a condiciones verificables)

Estas reglas se aplican en cada carga, antes de entrenar o puntuar el modelo de churn.
Si una regla falla, los datos **no** pasan al modelo: `train_models.py` se detiene.

| # | Regla de negocio | Condición verificable | Columnas |
|---|---|---|---|
| R1 | Ningún registro incompleto | Sin valores nulos | `client_id` y las 6 variables del modelo (+ `churned_3_months` en el histórico) |
| R2 | La antigüedad no puede ser negativa | `months_with_bank` ≥ 0 | `months_with_bank` |
| R3 | Los scores son proporciones | `product_usage_score` y `client_value_score` en [0, 1] | ambos scores |
| R4 | Conteos imposibles no se aceptan | Consultas a la competencia y quejas ≥ 0 | `competitor_rate_inquiries`, `complaint_count_last_year` |
| R5 | Formato correcto | Las variables del modelo son numéricas | las 6 variables del modelo |
| R6 | Un cliente aparece una sola vez por carga | `client_id` sin duplicados | `client_id` |
| R7 | El target es binario | `churned_3_months` ∈ {0, 1} | `churned_3_months` (solo histórico) |

`active_products_change_6m` puede ser negativo (el cliente cerró productos), por eso solo se exige que sea numérico.

## Variables derivadas (uso de producto y quejas)

| Variable | Fórmula | Para qué sirve |
|---|---|---|
| `complaints_per_month` | `complaint_count_last_year / months_with_bank` (antigüedad mínima 1 mes) | Intensidad de quejas ajustada por antigüedad: 2 quejas pesan más en un cliente de 3 meses que en uno de 10 años |
| `products_declining` | 1 si `active_products_change_6m` < 0, si no 0 | Señal temprana de fuga: el cliente está cerrando productos |
