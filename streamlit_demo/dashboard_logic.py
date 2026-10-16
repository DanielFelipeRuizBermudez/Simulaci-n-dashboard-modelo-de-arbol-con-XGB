"""
Lógica de los dashboards, separada de app.py para poder probarla sin Streamlit.
Sprint 2 · Tarea 6 · Delinquency Dashboard y Tarea 7 · Churn Dashboard.

- load_model / score_clients: carga el modelo y puntúa clientes (la usa app.py).
- model_version: versión del modelo y del dato que generó cada alerta.
- delinquency_alert_level: reglas de alerta 30/60 días.
- add_priority / prepare_delinquency_dashboard: lista priorizada por
  priority_score = risk_score × credit_exposure_cop.
- CHURN_KEY_FIELDS / churn_alert_driver / prepare_churn_dashboard: indicadores
  clave, priority_score = risk_score × client_value_score y la variable SHAP
  que dispara cada alerta de churn.
"""

import hashlib
import json
import os

import joblib
import pandas as pd

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_DIR = os.path.join(BASE_DIR, "models")
ALERT_DAYS_HIGH = 30
ALERT_DAYS_CRITICAL = 60
ALERT_LEVELS = ["critical", "high", "medium", "none"]  


def load_model(name, model_dir=MODEL_DIR):
    model = joblib.load(os.path.join(model_dir, f"{name}_model.pkl"))
    with open(os.path.join(model_dir, f"{name}_meta.json")) as f:
        meta = json.load(f)
    return model, meta


def score_clients(df, model, meta):
    """Probabilidad de riesgo por cliente y marca según el umbral del modelo."""
    proba = model.predict_proba(df[meta["features"]])[:, 1]
    out = df.copy()
    out["risk_score"] = proba
    out["flagged"] = out["risk_score"] >= meta["threshold"]
    return out.sort_values("risk_score", ascending=False)


def _short_hash(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()[:8]


def data_fingerprint(df):
    """Huella corta del lote de datos puntuado (cambia si cambia el archivo)."""
    raw = pd.util.hash_pandas_object(df, index=False).values.tobytes()
    return hashlib.sha256(raw).hexdigest()[:8]


def model_version(name, meta, model_dir=MODEL_DIR):
    """Identifica el modelo usado: archivo (hash), métrica y umbral."""
    metric = "F2" if "f2_score" in meta else "F1"
    score = meta.get("f2_score", meta.get("f1_score"))
    file_hash = _short_hash(os.path.join(model_dir, f"{name}_model.pkl"))
    return f"{name}-{file_hash} · {metric} {score:.2f} · umbral {meta['threshold']:.2f}"


def delinquency_alert_level(scored):
    """critical / high / medium para marcados según días de atraso; none si no está marcado."""
    days = scored["avg_days_late_last_year"]
    level = pd.Series("none", index=scored.index)
    level[scored["flagged"]] = "medium"
    level[scored["flagged"] & (days >= ALERT_DAYS_HIGH)] = "high"
    level[scored["flagged"] & (days >= ALERT_DAYS_CRITICAL)] = "critical"
    return level


def add_priority(scored, amount_col):
    """
    priority_score = probabilidad de riesgo × monto en juego.
    Orden: primero los clientes marcados por el modelo (las alertas), de mayor a
    menor prioridad; después los no marcados, también por prioridad.
    """
    out = scored.copy()
    out["priority_score"] = out["risk_score"] * out[amount_col]
    return out.sort_values(["flagged", "priority_score"], ascending=[False, False])


def prepare_delinquency_dashboard(scored, meta):
    out = add_priority(scored, meta.get("amount_column", "credit_exposure_cop"))
    out["alert_level"] = delinquency_alert_level(out)
    return out


CHURN_KEY_FIELDS = ["months_with_bank", "complaint_count_last_year", "product_usage_score"]


def churn_alert_driver(scored, shap_df):
    """
    Para cada cliente marcado, la variable con el mayor aporte SHAP positivo
    (la que más empuja su riesgo de fuga hacia arriba). Vacío si no está marcado.
    """
    shap_aligned = shap_df.loc[scored.index]
    driver = shap_aligned.idxmax(axis=1).where(shap_aligned.max(axis=1) > 0, "")
    return driver.where(scored["flagged"], "")


def prepare_churn_dashboard(scored, meta, shap_df):
    out = add_priority(scored, meta.get("amount_column", "client_value_score"))
    out["alert_driver"] = churn_alert_driver(out, shap_df)
    return out
