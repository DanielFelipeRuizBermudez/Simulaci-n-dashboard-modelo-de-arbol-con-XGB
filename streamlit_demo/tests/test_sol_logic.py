"""
Sol + cola de llamadas: priorización, verificación de identidad y escalamiento.
Sprint 3 · P1 (T8) · Sol + alertas.

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import os

import pandas as pd
import pytest

from dashboard_logic import load_model, prepare_delinquency_dashboard, score_clients
from sol_logic import (
    ACTION_HUMAN,
    ACTION_SOL,
    ESCALATION_EXPOSURE_COP,
    MAX_IDENTITY_ATTEMPTS,
    build_call_queue,
    escalation_reasons,
    needs_human_escalation,
    verify_identity,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture
def board():
    """Salida típica de prepare_delinquency_dashboard (ya trae priority_score)."""
    return pd.DataFrame({
        "client_id": ["A", "B", "C", "D", "E"],
        "risk_score": [0.90, 0.50, 0.40, 0.95, 0.35],
        "flagged": [True, True, True, False, True],
        "credit_exposure_cop": [1_000_000, 30_000_000, 2_000_000, 60_000_000, 4_000_000],
        "alert_level": ["critical", "high", "medium", "none", "medium"],
        "priority_score": [900_000, 15_000_000, 800_000, 57_000_000, 1_400_000],
    })


# --- Cola de llamadas -------------------------------------------------------

def test_cola_solo_incluye_clientes_marcados(board):
    queue = build_call_queue(board)
    assert "D" not in queue["client_id"].tolist()
    assert queue["flagged"].all()


def test_cola_ordenada_por_prioridad_riesgo_por_exposicion(board):
    queue = build_call_queue(board)
    assert queue["client_id"].tolist() == ["B", "E", "A", "C"]


def test_cola_numera_las_posiciones_desde_1(board):
    queue = build_call_queue(board)
    assert queue["queue_position"].tolist() == [1, 2, 3, 4]


def test_cola_respeta_el_tope_de_llamadas(board):
    queue = build_call_queue(board, top_n=2)
    assert queue["client_id"].tolist() == ["B", "E"]


def test_exposicion_alta_va_directo_a_asesor_humano(board):
    queue = build_call_queue(board).set_index("client_id")
    assert board.loc[1, "credit_exposure_cop"] > ESCALATION_EXPOSURE_COP
    assert queue.loc["B", "sol_action"] == ACTION_HUMAN
    assert queue.loc["A", "sol_action"] == ACTION_SOL


def test_cola_vacia_si_no_hay_alertas(board):
    board["flagged"] = False
    queue = build_call_queue(board)
    assert queue.empty
    assert "queue_position" in queue.columns


# --- Verificación de identidad ---------------------------------------------

def test_identidad_verificada_si_coinciden_los_dos_datos():
    expected = {"document_last4": "4821", "birth_year": 1985}
    assert verify_identity(expected, {"document_last4": "4821", "birth_year": "1985"})


def test_identidad_no_verificada_si_falla_un_dato():
    expected = {"document_last4": "4821", "birth_year": 1985}
    assert not verify_identity(expected, {"document_last4": "4821", "birth_year": 1990})


def test_identidad_no_verificada_si_falta_un_dato():
    expected = {"document_last4": "4821", "birth_year": 1985}
    assert not verify_identity(expected, {"document_last4": "4821"})


# --- Escalamiento a asesor humano ------------------------------------------

def test_escala_tras_dos_intentos_fallidos_de_verificacion():
    assert MAX_IDENTITY_ATTEMPTS == 2
    assert not needs_human_escalation(failed_attempts=1)
    assert needs_human_escalation(failed_attempts=2)


def test_escala_si_el_cliente_pide_un_asesor():
    assert needs_human_escalation(client_requested_human=True)


def test_escala_si_la_exposicion_supera_el_umbral():
    assert needs_human_escalation(exposure_cop=ESCALATION_EXPOSURE_COP + 1)
    assert not needs_human_escalation(exposure_cop=ESCALATION_EXPOSURE_COP)


def test_razones_de_escalamiento_explican_la_decision():
    reasons = escalation_reasons(failed_attempts=2, client_requested_human=True)
    assert len(reasons) == 2
    assert escalation_reasons() == []


# --- Integración con el modelo real ----------------------------------------

def test_cola_con_predicciones_del_modelo_de_mora():
    model, meta = load_model("delinquency")
    clients = pd.read_csv(os.path.join(DATA_DIR, "new_clients_template.csv"))
    board = prepare_delinquency_dashboard(score_clients(clients, model, meta), meta)
    queue = build_call_queue(board)
    assert len(queue) == int(board["flagged"].sum())
    assert queue["priority_score"].is_monotonic_decreasing
    assert set(queue["sol_action"]) <= {ACTION_SOL, ACTION_HUMAN}
