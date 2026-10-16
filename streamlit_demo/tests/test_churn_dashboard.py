"""
Dashboard de churn: indicadores clave, priorización, variable SHAP que dispara
la alerta y conexión con el modelo.
Sprint 2 · Tarea 7 · Churn Dashboard.

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import os

import pandas as pd
import pytest
import shap

from dashboard_logic import (
    CHURN_KEY_FIELDS,
    churn_alert_driver,
    load_model,
    prepare_churn_dashboard,
    score_clients,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture
def scored():
    return pd.DataFrame({
        "client_id": ["A", "B", "C"],
        "risk_score": [0.8, 0.4, 0.05],
        "flagged": [True, True, False],
        "client_value_score": [0.1, 0.9, 0.9],
    })


@pytest.fixture
def shap_df(scored):
    return pd.DataFrame({
        "product_usage_score": [0.50, -0.10, 0.30],
        "complaint_count_last_year": [0.20, 0.40, 0.10],
    }, index=scored.index)


# --- Indicadores de riesgo y campos clave -------------------------------------------
def test_campos_clave_son_variables_del_modelo():
    _, meta = load_model("churn")
    assert set(CHURN_KEY_FIELDS) <= set(meta["features"])
    assert CHURN_KEY_FIELDS == ["months_with_bank", "complaint_count_last_year", "product_usage_score"]


# --- Fórmula de priorización (score × valor del cliente) -----------------------------
def test_priority_score_es_riesgo_por_valor_del_cliente(scored, shap_df):
    out = prepare_churn_dashboard(scored, {"amount_column": "client_value_score"}, shap_df)
    out = out.set_index("client_id")
    assert out.loc["B", "priority_score"] == pytest.approx(0.4 * 0.9)


def test_lista_prioriza_clientes_marcados_de_mayor_valor(scored, shap_df):
    out = prepare_churn_dashboard(scored, {"amount_column": "client_value_score"}, shap_df)
    # B: 0.36 > A: 0.08 (A tiene más riesgo pero vale menos); C no está marcado
    assert out["client_id"].tolist() == ["B", "A", "C"]


# --- Variable SHAP que dispara la alerta -------------------------------------------------
def test_variable_que_dispara_la_alerta(scored, shap_df):
    drivers = churn_alert_driver(scored, shap_df).tolist()
    # A: uso de productos (0.50) · B: quejas (0.40) · C: no está marcado -> vacío
    assert drivers == ["product_usage_score", "complaint_count_last_year", ""]


# --- Test de conexión modelo -> dashboard ----------------------------------------------
def test_dashboard_recibe_predicciones_y_explicaciones_del_modelo():
    model, meta = load_model("churn")
    clients = pd.read_csv(os.path.join(DATA_DIR, "new_clients_template.csv"))
    scored = score_clients(clients, model, meta)
    values = shap.TreeExplainer(model).shap_values(scored[meta["features"]].astype(float))
    shap_df = pd.DataFrame(values, columns=meta["features"], index=scored.index)

    board = prepare_churn_dashboard(scored, meta, shap_df)
    assert len(board) == len(clients) > 0
    assert board["risk_score"].between(0, 1).all()
    flagged = board[board["flagged"]]
    assert (flagged["alert_driver"].isin(meta["features"])).all()
