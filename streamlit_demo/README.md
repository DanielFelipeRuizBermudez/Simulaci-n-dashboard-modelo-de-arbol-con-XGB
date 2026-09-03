# FinBank Predictive Analytics — Demo Streamlit

Demo funcional para la sustentación: sube un archivo de clientes nuevos y ve
la predicción de riesgo (mora o churn) al instante, con KPIs, la lista
priorizada, una explicación SHAP de por qué se marcó cada cliente, y un chat
con Sol (Gemini) que puede responder preguntas concretas sobre los
resultados.

⚠️ **Importante:** este código no se pudo ejecutar completo dentro del
entorno de Claude porque no tiene acceso a internet para instalar
`xgboost`, `shap`, `streamlit` ni `google-genai`. Tienes que correrlo en tu
computador (o en Streamlit Community Cloud, que sí tiene internet). La
lógica de entrenamiento, grid search y umbral (F2/F1) sí se probó y
funciona correctamente con un modelo equivalente de sklearn — falta correrla
con XGBoost real en tu máquina.

## Qué cambió en esta versión

1. **Una sola base de clientes**, no dos separadas. `historical_data.csv`
   tiene todas las columnas (features de mora + features de churn) y las
   dos variables de respuesta (`defaulted_30_60_days`, `churned_3_months`).
   Cada modelo simplemente usa su propia variable de respuesta y su propio
   subconjunto de columnas — igual que pasaría con un extracto real de
   FinBank.
2. **Grid search de hiperparámetros** en `train_models.py`: prueba
   combinaciones de `max_depth`, `learning_rate`, `n_estimators` y
   `scale_pos_weight` (este último ayuda específicamente con el
   desbalance de clases), y se queda con la combinación que da el mejor
   F2 (mora) o F1 (churn) — nunca con la de mejor accuracy.
3. **Sol ahora usa "tools" reales**, no un resumen de texto. Cuando le
   preguntan "dame 10 clientes para llamar" o "¿cuántos están en riesgo de
   churn?", Gemini llama automáticamente a una función de Python que lee el
   DataFrame real y le devuelve datos exactos — no inventa números ni IDs
   de clientes.
4. **Un solo archivo de "clientes nuevos"** (`new_clients_template.csv`),
   que sirve para las dos pestañas (Delinquency y Churn), ya que tiene
   todas las columnas de ambos modelos.

## Sobre de dónde salen los datos de entrenamiento

Como es un proyecto de simulación y no tienen acceso a datos reales de
FinBank, usar datos sintéticos es la práctica esperada para este tipo de
demo — no hay nada que "conseguir" aparte de lo que ya generamos. El
desbalance de clases se mantuvo realista (~18% de mora, ~15% de churn),
similar al rango reportado en la literatura de scoring crediticio (7%-22%
según el dataset).

**Si más adelante quieren usar datos reales** (por ejemplo, para el
capstone o para verse aún más creíbles), existe un dataset público real
citado en el mismo paper académico que respalda XGBoost+SHAP: "Default of
Credit Card Clients" (UCI Machine Learning Repository) — pero para la
demo de mañana, lo sintético que ya está armado es más que suficiente.

## Cómo correrlo (en tu computador)

1. Instala Python 3.10+ si no lo tienes.
2. Abre una terminal en esta carpeta y corre:

```bash
pip install -r requirements.txt
```

3. Genera los datos sintéticos (ya vienen generados en `/data`, pero puedes
   regenerarlos si quieres):

```bash
python generate_data.py
```

4. Entrena los dos modelos con grid search (esto crea los archivos en
   `/models` — puede tardar 1-2 minutos porque prueba varias combinaciones
   de hiperparámetros):

```bash
python train_models.py
```

Deberías ver algo como:
```
[delinquency] Trying 24 hyperparameter combinations...
[delinquency] best params={'max_depth': ..., 'learning_rate': ..., ...}
[delinquency] threshold=0.XX  F2-score=0.XXXX
[churn] Trying 24 hyperparameter combinations...
[churn] threshold=0.XX  F1-score=0.XXXX
```

5. Corre la app:

```bash
streamlit run app.py
```

Se abre automáticamente en el navegador (normalmente en `http://localhost:8501`).

## Cómo hacer la demo en vivo

1. En cada pestaña (Delinquency / Churn) hay un botón para descargar el
   archivo de ejemplo de "clientes nuevos" (`new_clients_template.csv`,
   funciona en las dos pestañas).
2. Súbelo con el botón de "Upload new client data".
3. Verás automáticamente KPIs, la lista priorizada, la distribución de
   riesgo, y la explicación SHAP al seleccionar un cliente.
4. Ve a la pestaña "💬 Ask Sol", pega tu API key de Gemini en la barra
   lateral, y pregúntale cosas como:
   - *"How many clients were flagged as high risk?"*
   - *"Give me a list of 10 delinquency clients to call, sorted by risk."*
   - *"Which client has the highest churn risk right now?"*

   Como Sol usa herramientas reales conectadas a tus datos, las respuestas
   van a tener IDs de clientes reales de tu archivo subido, no inventados.

## Sobre tu API key de Google AI (la de los 40k COP)

Los créditos prepago de Gemini API expiran a los **12 meses** de la compra,
no cada mes. Los 40k los tienes disponibles todo ese año sin necesidad de
recargar mensualmente. El consumo de esta demo (unas preguntas de texto con
el modelo "flash", el más barato) es mínimo.

## Si quieren usar sus propios datos de ejemplo

El archivo subido debe tener, como mínimo, estas columnas (revisa
`new_clients_template.csv` para el formato exacto):

`monthly_income_cop`, `credit_exposure_cop`, `avg_days_late_last_year`,
`num_active_products`, `credit_utilization`, `months_with_bank`,
`product_usage_score`, `competitor_rate_inquiries`,
`complaint_count_last_year`, `active_products_change_6m`,
`client_value_score`

(La pestaña de Delinquency solo usa las primeras 6; la de Churn usa
`months_with_bank` + las últimas 5 — pero como el archivo de ejemplo trae
todas, funciona igual en ambas.)

## Nota para la sustentación

Todos los datos (históricos y de clientes nuevos) son **sintéticos**,
generados para que la demo se vea realista — no son datos reales de FinBank.
Es honesto (y más seguro) decir esto explícitamente si preguntan: "This is a
working prototype built on synthetic data representative of a banking
portfolio, showing exactly how the final product would function."
