# Simulación Dashboard — Modelo de Árbol con XGBoost

Demo interactivo en Streamlit que simula un producto de analítica predictiva
bancaria: dos modelos XGBoost (morosidad temprana y deserción/churn de
clientes), explicabilidad con SHAP, y un asistente conversacional (Sol,
potenciado por la API de Gemini) que responde preguntas en lenguaje natural
sobre los resultados usando herramientas conectadas a los datos reales de la
sesión.

## Qué incluye

- **Dos modelos XGBoost** (morosidad a 30/60 días y churn a 3 meses),
  entrenados con grid search de hiperparámetros y umbral de decisión
  optimizado por F2/F1 (no por accuracy), sobre datos sintéticos
  representativos de un portafolio bancario.
- **Explicabilidad con SHAP**: gráfico beeswarm global (qué variables
  influyen más y en qué dirección) y desglose local por cliente.
- **KPIs y dona de riesgo interactiva** (Plotly) con el porcentaje de
  clientes marcados como alto riesgo.
- **Carga automática de datos de ejemplo** al abrir cada pestaña, con
  botones para quitar los datos cargados o restaurar el ejemplo, además del
  uploader para subir tu propio CSV.
- **Interfaz bilingüe** (español/inglés) mediante un selector en la barra
  lateral.
- **Sol**, el chat de Gemini: detecta automáticamente el idioma de cada
  pregunta y responde en ese idioma (independiente del idioma de la
  interfaz), usando funciones de Python como herramientas para consultar
  KPIs, listas de clientes y contribuciones SHAP reales — nunca inventa
  números ni IDs de clientes.

## Estructura del proyecto

```
streamlit_demo/
├── app.py                      # App principal de Streamlit
├── generate_data.py             # Genera los datos sintéticos de entrenamiento
├── train_models.py              # Entrena ambos modelos XGBoost (grid search)
├── validation.py                # Reglas de calidad de datos (Sprint 1)
├── evaluate_models.py           # Reportes de validación de los modelos (Sprint 2)
├── dashboard_logic.py           # Alertas, priorización y versión del modelo (Sprint 2)
├── requirements.txt
├── data/
│   ├── historical_data.csv          # Base histórica sintética (entrenamiento)
│   └── new_clients_template.csv     # Ejemplo de clientes nuevos para calificar
├── models/                      # Modelos entrenados (versionados en el repo)
├── reports/                     # Reportes JSON de validación de los modelos
├── docs/                        # Reglas de validación y documentación de los modelos
├── tests/                       # Pruebas automatizadas (pytest)
├── assets/
│   └── logo.jpg
└── .streamlit/
    ├── config.toml
    └── secrets.toml             # Tu API key de Gemini (no versionado)
```

## Cómo correrlo

1. Clona el repo e instala las dependencias:

   ```bash
   cd streamlit_demo
   pip install -r requirements.txt
   ```

2. Los modelos ya entrenados están en `models/`. Para regenerar los datos y
   reentrenarlos:

   ```bash
   python generate_data.py
   python train_models.py
   ```

3. Configura tu API key de Gemini para el chat de Sol. Crea el archivo
   `streamlit_demo/.streamlit/secrets.toml` (este archivo está en
   `.gitignore`, nunca se sube) con:

   ```toml
   GEMINI_API_KEY = "tu_api_key_aqui"
   ```

   Consigue una key gratis en [aistudio.google.com](https://aistudio.google.com).
   Si no configuras este archivo, la app sigue funcionando igual, solo que
   te pedirá pegar la key manualmente en la barra lateral cuando abras la
   pestaña "Ask Sol".

4. Corre la app:

   ```bash
   python -m streamlit run app.py
   ```

   Se abre en `http://localhost:8501`.

5. Corre las pruebas automatizadas (también corren en GitHub Actions en cada
   Pull Request):

   ```bash
   pytest -v
   ```

## Gestión del proyecto (Corte 2)

La documentación Scrum/XP está en [`docs/`](docs/README.md): Sprints, Velocity y
Burndown, Dailies, Retrospectivas y la bitácora de prácticas XP.

## Nota sobre los datos

Todos los datos (históricos y de clientes nuevos) son **sintéticos**,
generados para que la demo se vea realista — no son datos reales de
FinBank. El desbalance de clases se mantuvo realista (~18% de mora, ~15%
de churn), similar al rango reportado en la literatura de scoring
crediticio.
