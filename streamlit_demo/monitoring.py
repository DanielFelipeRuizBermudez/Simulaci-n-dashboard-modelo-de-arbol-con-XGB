"""
Monitoreo post-despliegue: estabilidad de los datos frente a los de
entrenamiento, separado de app.py para poder probarlo sin Streamlit.
Sprint 3 · P3 (T10) · Monitoreo del modelo.

- psi: índice de estabilidad poblacional (PSI) de una variable entre los
  datos de entrenamiento y un lote nuevo.
- psi_status: semáforo del PSI (verde, amarillo, rojo).
- drift_report: PSI y semáforo de cada variable de los modelos.
- needs_retraining: True si alguna variable está en rojo.
- simulate_drift: lote desplazado para la demo y las pruebas.
"""

import numpy as np
import pandas as pd

# Umbrales usuales en riesgo de crédito.
PSI_YELLOW = 0.10
PSI_RED = 0.25

STATUS_GREEN = "green"
STATUS_YELLOW = "yellow"
STATUS_RED = "red"

# Número máximo de rangos y mínimo de clientes del lote nuevo por rango.
MAX_BINS = 10
MIN_CLIENTS_PER_BIN = 10

# Evita log(0) y divisiones por cero cuando un rango queda vacío.
EPSILON = 1e-4


def _bin_edges(reference, bins):
    """Cortes por cuantiles de los datos de entrenamiento (sin repetir)."""
    quantiles = np.linspace(0, 1, bins + 1)
    edges = np.unique(np.quantile(reference, quantiles))
    edges[0], edges[-1] = -np.inf, np.inf
    return edges


def _bins_for(n_new):
    """Menos rangos para lotes pequeños, para no confundir ruido con cambio."""
    return int(max(2, min(MAX_BINS, n_new // MIN_CLIENTS_PER_BIN)))


def psi(reference, new, bins=None):
    """
    PSI = suma de (% nuevo - % entrenamiento) * ln(% nuevo / % entrenamiento)
    sobre rangos definidos con los cuantiles de los datos de entrenamiento.
    """
    reference = pd.Series(reference, dtype=float).dropna().to_numpy()
    new = pd.Series(new, dtype=float).dropna().to_numpy()
    if len(reference) == 0 or len(new) == 0:
        raise ValueError("PSI necesita datos de entrenamiento y del lote nuevo")
    if bins is None:
        bins = _bins_for(len(new))
    edges = _bin_edges(reference, bins)
    if len(edges) < 2:
        return 0.0
    ref_pct = np.histogram(reference, edges)[0] / len(reference)
    new_pct = np.histogram(new, edges)[0] / len(new)
    ref_pct = np.clip(ref_pct, EPSILON, None)
    new_pct = np.clip(new_pct, EPSILON, None)
    return float(np.sum((new_pct - ref_pct) * np.log(new_pct / ref_pct)))


def psi_status(value):
    """Verde < 0.10 (estable), amarillo 0.10–0.25 (vigilar), rojo > 0.25 (reentrenar)."""
    if value > PSI_RED:
        return STATUS_RED
    if value >= PSI_YELLOW:
        return STATUS_YELLOW
    return STATUS_GREEN


def drift_report(reference_df, new_df, features):
    """PSI y semáforo por variable, de mayor a menor PSI."""
    rows = []
    for feature in features:
        if feature not in reference_df.columns or feature not in new_df.columns:
            continue
        value = psi(reference_df[feature], new_df[feature])
        rows.append({"feature": feature, "psi": value, "status": psi_status(value)})
    report = pd.DataFrame(rows, columns=["feature", "psi", "status"])
    return report.sort_values("psi", ascending=False).reset_index(drop=True)


def needs_retraining(report):
    """True si al menos una variable está en rojo."""
    return bool((report["status"] == STATUS_RED).any())


def simulate_drift(df):
    """
    Lote desplazado para la demo: clientes con menos ingreso, más uso del
    cupo y más días de atraso que en el entrenamiento.
    """
    shifted = df.copy()
    if "monthly_income_cop" in shifted:
        shifted["monthly_income_cop"] = shifted["monthly_income_cop"] * 0.6
    if "credit_utilization" in shifted:
        shifted["credit_utilization"] = (shifted["credit_utilization"] + 0.3).clip(upper=1.0)
    if "avg_days_late_last_year" in shifted:
        shifted["avg_days_late_last_year"] = shifted["avg_days_late_last_year"] + 10
    return shifted
