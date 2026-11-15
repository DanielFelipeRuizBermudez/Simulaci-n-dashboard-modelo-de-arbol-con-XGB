"""
Validación end to end: Flujo desde datos, validación, modelo, alertas y cola de Sol

Se realizan pruebas del sstema completo antes de lanzar una versión.

Ejecutsr desde streamlit_demo/:
    pytest tests/test_e2e.py -v
"""

import os

import pandas as pd
import pytest

from dashboard_logic import load_model, prepare_delinquency_dashboard, score_clients
from sol_logic import ACTION_HUMAN, ACTION_SOL, build_call_queue
from validation import validate_delinquency_data

data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
historical = os.path.join(data_dir, "historical_data.csv")

@pytest.fixture(scope="module")
def clients():
    return pd.read_csv(historical)

@pytest.fixture(scope="module")
def pipeline(clients):
    """Corre todo el flujo de mora una sola y devuelve cada etapa"""
    errors = validate_delinquency_data(clients)
    model, meta = load_model("delinquency")
    scored = score_clients(clients, model, meta)
    board = prepare_delinquency_dashboard(scored, meta)
    queue = build_call_queue(board)
    return {"errors": errors, "scored": scored, "board": board, "queue": queue}

def test_datos_ejemplo_pasan_validacion(pipeline):
    assert pipeline["errors"] == []

def test_modelo_puntua_todos_los_clientes(clients, pipeline):
    scored = pipeline["scored"]
    assert len(scored) == len(clients)
    assert scored["risk_score"].between(0, 1).all()

def test_tablero_da_alerta_y_prioridad(pipeline):
    board = pipeline["board"]
    assert {"flagged", "alert_level", "priority_score"} <= set(board.columns)
    assert board["flagged"].any()

def test_cola_de_sol_tiene_clientes_marcados(pipeline):
    queue = pipeline["queue"]
    assert len(queue) > 0
    assert queue["flagged"].all()
    assert (queue["alert_level"] != "none").all()

def test_cola_ordenada_por_prioridad(pipeline):
    queue = pipeline["queue"]
    assert queue["priority_score"].is_monotonic_decreasing
    assert queue["queue_position"].to_list() == list(range(1, len(queue) + 1))

def test_cada_cliente_cola_de_la_cola_tiene_quien_lo_llama(pipeline):
    assert set(pipeline["queue"]["sol_action"]) <= {ACTION_SOL, ACTION_HUMAN}

def test_lote_invalido_bloqueado_antes_de_prediccion(clients):
    """ Si los datos no pasan validación, el flujo no debe llegar al modelo """
    bad = clients.head(50).copy()
    bad.loc[bad.index[0], "credit_utilization"] = 5 # Está fuera de rango ya que es entre 0 y 1 
    bad.loc[bad.index[1], "monthly_income_cop"] = None 
    errors = validate_delinquency_data(bad)
    assert errors, "Lote inválido debería producir errores de validación"