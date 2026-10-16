"""
Dashboard de mora: reglas de alerta, priorización, versión y conexión con el modelo.
Sprint 2 · Tarea 6 · Delinquency Dashboard.

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import os

import pandas as pd
import pytest

from dashboard_logic import (
    ALERT_DAYS_CRITICAL,
    ALERT_DAYS_HIGH,
    add_priority,
    delinquency_alert_level,
    load_model,
    model_version,
    prepare_delinquency_dashboard,
    score_clients,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture
def scored():
    return pd.DataFrame({
        "client_id": ["A", "B", "C", "D"],
        "risk_score": [0.9, 0.5, 0.4, 0.1],
        "flagged": [True, True, True, False],
        "avg_days_late_last_year": [75.0, 35.0, 5.0, 80.0],
        "credit_exposure_cop": [1_000_000, 10_000_000, 2_000_000, 60_000_000],
    })


# --- Reglas de alerta 30/60 días ---------------------------------------------------
def test_umbrales_de_alerta_son_30_y_60_dias():
    assert (ALERT_DAYS_HIGH, ALERT_DAYS_CRITICAL) == (30, 60)


def test_niveles_de_alerta(scored):
    levels = delinquency_alert_level(scored).tolist()
    # A: marcado y 75 días -> crítica; B: 35 días -> alta; C: 5 días -> media;
    # D: 80 días pero NO marcado por el modelo -> sin alerta
    assert levels == ["critical", "high", "medium", "none"]


# --- Fórmula de priorización (score × exposición) ---------------------------------
def test_priority_score_es_riesgo_por_exposicion(scored):
    out = add_priority(scored, "credit_exposure_cop").set_index("client_id")
    assert out.loc["B", "priority_score"] == pytest.approx(0.5 * 10_000_000)


def test_lista_ordenada_por_prioridad(scored):
    out = prepare_delinquency_dashboard(scored, {"amount_column": "credit_exposure_cop"})
    # B: 0.5 × 10M = 5M · A: 0.9 × 1M = 0.9M · C: 0.4 × 2M = 0.8M · D: 0.1 × 60M = 6M
    # B supera a A aunque A tiene más riesgo, porque hay más dinero en juego.
    # D tiene la prioridad más alta, pero el modelo no lo marcó: va al final.
    assert out["client_id"].tolist() == ["B", "A", "C", "D"]


# --- Versión del modelo por alerta -------------------------------------------------
def test_version_del_modelo_identifica_archivo_metrica_y_umbral():
    _, meta = load_model("delinquency")
    version = model_version("delinquency", meta)
    assert version.startswith("delinquency-")
    assert "F2" in version and "umbral" in version


# --- Test de conexión modelo -> dashboard -----------------------------------------
def test_dashboard_recibe_predicciones_del_modelo_cargado():
    model, meta = load_model("delinquency")
    clients = pd.read_csv(os.path.join(DATA_DIR, "new_clients_template.csv"))
    board = prepare_delinquency_dashboard(score_clients(clients, model, meta), meta)
    assert len(board) == len(clients) > 0
    assert board["risk_score"].between(0, 1).all()
    assert board["priority_score"].notna().all()
    assert set(board["alert_level"]) <= {"critical", "high", "medium", "none"}
