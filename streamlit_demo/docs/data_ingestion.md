# Data Ingestion Pipeline

Tarea 1 · Sprint 1 · Data Ingestion Pipeline
Autor: Daniel · Revisa: Michelle

El pipeline de ingesta extrae la información de clientes de FinBank y la deja en una sola tabla por cliente, de la cual cada modelo toma sus variables y su variable respuesta. El proceso vive en `streamlit_demo/generate_data.py` y la carga de clientes nuevos se hace desde `streamlit_demo/app.py`.

## Cumplimiento de las subtareas de Trello

| Subtarea de Trello | Cómo se cumple | Dónde |
|---|---|---|
| Identify the data sources (payment history, product usage, customer demographics) in collaboration with FinBank's IT team | Se definieron tres fuentes y se integran en una tabla única por `client_id`: **historial de pago y crédito** (`avg_days_late_last_year`, `credit_utilization`, `credit_exposure_cop`, `monthly_income_cop`), **relación con el banco** (`months_with_bank`, `num_active_products`, `active_products_change_6m`) y **uso de producto y servicio** (`product_usage_score`, `competitor_rate_inquiries`, `complaint_count_last_year`, `client_value_score`) | `generate_customers()` en `generate_data.py` |
| Define the frequency at which each source is extracted (in real time) | El histórico se extrae en una carga completa para entrenar los modelos. Los clientes nuevos se procesan en el momento en que se cargan en el dashboard: la app los recibe, los puntúa con el modelo y muestra el resultado de inmediato | `generate_data.py` (histórico) y cargador de archivos de `app.py` (clientes nuevos) |
| Create the extraction process using automated programming | Un solo comando, `python generate_data.py`, ejecuta la extracción completa y escribe los archivos de salida en `data/`. Usa una semilla fija (`np.random.seed(42)`), así cada ejecución produce exactamente la misma carga y los resultados son reproducibles | `generate_data.py` |
| Set up pipeline failure alerts, so extraction issues are caught before they reach validation | Al cargar un archivo, la app verifica que traiga todas las columnas que usa el modelo. Si falta alguna, detiene el proceso y muestra cuáles faltan, antes de que los datos lleguen al modelo. Si el modelo entrenado no está disponible, muestra una advertencia en lugar de continuar | `app.py` (mensajes `missing_columns` y `model_not_found`) |

## Archivos de salida

| Archivo | Registros | Contenido |
|---|---|---|
| `data/historical_data.csv` | 6.000 clientes | `client_id`, 11 variables predictoras y las dos variables respuesta: `defaulted_30_60_days` (mora 30/60 días) y `churned_3_months` (fuga a 3 meses) |
| `data/new_clients_template.csv` | 40 clientes | Las mismas variables sin variables respuesta, para cargar y puntuar clientes nuevos |

La proporción de clases se mantiene en niveles de cartera reales: entre 15 % y 20 % de mora y entre 12 % y 16 % de fuga.

## Siguiente paso del pipeline

Los datos extraídos pasan a la etapa de validación y limpieza (Tareas 2 y 3 del Sprint 1), donde `validation.py` revisa nulos, rangos, duplicados y formato antes de entrenar los modelos.
