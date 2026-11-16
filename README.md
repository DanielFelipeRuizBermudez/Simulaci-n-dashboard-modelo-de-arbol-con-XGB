# Simulación Dashboard — Modelo de Árbol con XGBoost

Demo interactivo en Streamlit que simula un producto de analítica predictiva
bancaria: dos modelos XGBoost (morosidad temprana y deserción/churn de
clientes), explicabilidad con SHAP, y un asistente conversacional (Sol,
potenciado por la API de Gemini) que responde preguntas en lenguaje natural
sobre los resultados usando herramientas conectadas a los datos reales de la
sesión.

**Versión 1.0 publicada:** https://simulaci-n-dashboard-modelo-de-arbol-con-xgb-jsj2fqdjxrjrph7yd.streamlit.app/

Proyecto de FinTech Solutions para FinBank S.A. Los cambios de cada versión están en
[`CHANGELOG.md`](CHANGELOG.md).

## Manual corto de uso

La app abre con un lote de ejemplo de 40 clientes nuevos ya cargado en cada pestaña.

| Pestaña | Para qué sirve | Cómo usarla |
|---|---|---|
| **Morosidad** | Clientes con riesgo de mora a 30/60 días, priorizados por riesgo × exposición | Revisa los KPIs, la lista priorizada y la explicación SHAP de cada cliente. Abajo está la **Cola de llamadas de Sol**: el orden en que Sol llama y qué casos pasan a un asesor humano. |
| **Deserción** | Clientes con riesgo de irse en los próximos 3 meses | Revisa la lista priorizada por valor del cliente y la variable que más pesa en cada alerta. |
| **Monitoreo** | Saber si los datos nuevos se alejan de los del entrenamiento (PSI) | Mira el semáforo por variable: verde estable, amarillo vigilar, rojo reentrenar. Activa **Simular un lote desplazado** para ver cómo se ve una alerta roja. |
| **Pregúntale a Sol** | Preguntas en lenguaje natural sobre los resultados | Pega tu API key de Gemini en la barra lateral y pregunta, por ejemplo, "¿a quién llamo primero?". |

Para calificar tus propios clientes, sube un CSV con las mismas columnas de
`streamlit_demo/data/new_clients_template.csv`. Si los datos no pasan las reglas de calidad,
la app no los envía al modelo.

### Alcance de Sol en la versión 1.0

- **Hoy (v1.0):** asistente de **texto** dentro del dashboard. Consulta KPIs, listas de clientes,
  explicaciones SHAP y su propia cola de llamadas, y sigue un protocolo: verifica identidad con dos
  datos antes de hablar de la cuenta y escala a un asesor humano si la verificación falla dos veces,
  si el cliente lo pide o si la exposición supera $10,000,000 COP.
- **Siguiente fase:** canal de **voz** para que Sol haga las llamadas de cobranza preventiva,
  conectado a los sistemas reales de FinBank.

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
- **Cola de llamadas de Sol** (Sprint 3): clientes marcados en orden de prioridad, con
  verificación de identidad y escalamiento a asesor humano.
- **Monitoreo post-despliegue** (Sprint 3): PSI por variable frente a los datos de
  entrenamiento, con semáforo y recomendación de reentrenar.
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
├── sol_logic.py                 # Cola de llamadas, identidad y escalamiento de Sol (Sprint 3)
├── monitoring.py                # PSI y semáforo de monitoreo (Sprint 3)
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
   Pull Request, en dos pasos: unitarias y de punta a punta):

   ```bash
   pytest -v
   ```

   La versión 1.0 tiene 93 pruebas: 84 unitarias y 9 de punta a punta y de humo de la app.

## Gestión del proyecto (Cortes 2 y 3)

La documentación Scrum/XP está en [`docs/`](docs/README.md): Sprints, Velocity y
Burndown, Dailies, Retrospectivas y la bitácora de prácticas XP de los Sprints 1, 2 y 3.

## Nota sobre los datos

Todos los datos (históricos y de clientes nuevos) son **sintéticos**,
generados para que la demo se vea realista — no son datos reales de
FinBank. El desbalance de clases se mantuvo realista (~18% de mora, ~15%
de churn), similar al rango reportado en la literatura de scoring
crediticio.
