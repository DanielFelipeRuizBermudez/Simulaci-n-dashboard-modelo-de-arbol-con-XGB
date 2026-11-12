"""
Reglas de Sol para la intervención de cobranza, separadas de app.py para
poder probarlas sin Streamlit.
Sprint 3 · P1 (T8) · Sol + alertas.

- build_call_queue: cola de llamadas de Sol con los clientes marcados por el
  modelo de mora, ordenada por priority_score = riesgo × exposición.
- verify_identity: Sol no revela información de la cuenta sin que coincidan
  dos datos del cliente.
- escalation_reasons / needs_human_escalation: cuándo la llamada pasa a un
  asesor humano.
"""

import pandas as pd

# Exposición desde la cual el caso lo atiende directamente un asesor humano.
# Equivale aproximadamente al percentil 90 de la exposición de la cartera
# sintética (9.9M COP); se ajusta con datos reales de FinBank.
ESCALATION_EXPOSURE_COP = 10_000_000

# Intentos fallidos de verificación de identidad antes de escalar.
MAX_IDENTITY_ATTEMPTS = 2

# Datos que el cliente debe confirmar para verificar su identidad.
IDENTITY_FIELDS = ("document_last4", "birth_year")

ACTION_SOL = "sol"
ACTION_HUMAN = "human"

REASON_IDENTITY = "identity_failed"
REASON_REQUESTED = "client_requested"
REASON_EXPOSURE = "high_exposure"


def build_call_queue(board, top_n=None, amount_col="credit_exposure_cop"):
    """
    Cola de llamadas de Sol a partir del tablero de mora.

    Solo entran los clientes marcados por el modelo (las alertas), de mayor a
    menor priority_score. Cada fila trae su posición en la cola y la acción:
    'sol' si Sol puede hacer la llamada, 'human' si por exposición alta la
    atiende directamente un asesor.
    """
    queue = board[board["flagged"]].sort_values("priority_score", ascending=False)
    if top_n is not None:
        queue = queue.head(top_n)
    queue = queue.copy()
    queue["queue_position"] = range(1, len(queue) + 1)
    queue["sol_action"] = [
        ACTION_HUMAN if exposure > ESCALATION_EXPOSURE_COP else ACTION_SOL
        for exposure in queue[amount_col]
    ]
    return queue


def _normalize(value):
    return str(value).strip().lower() if value is not None else None


def verify_identity(expected, provided, fields=IDENTITY_FIELDS):
    """True solo si el cliente confirma todos los datos de identidad pedidos."""
    for field in fields:
        given = provided.get(field)
        if given is None or _normalize(given) != _normalize(expected.get(field)):
            return False
    return True


def escalation_reasons(failed_attempts=0, client_requested_human=False, exposure_cop=0.0):
    """Lista de razones por las que la llamada debe pasar a un asesor humano."""
    reasons = []
    if failed_attempts >= MAX_IDENTITY_ATTEMPTS:
        reasons.append(REASON_IDENTITY)
    if client_requested_human:
        reasons.append(REASON_REQUESTED)
    if exposure_cop > ESCALATION_EXPOSURE_COP:
        reasons.append(REASON_EXPOSURE)
    return reasons


def needs_human_escalation(failed_attempts=0, client_requested_human=False, exposure_cop=0.0):
    """True si se cumple al menos una regla de escalamiento."""
    return bool(escalation_reasons(failed_attempts, client_requested_human, exposure_cop))
