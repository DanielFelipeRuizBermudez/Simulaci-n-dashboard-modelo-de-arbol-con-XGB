"""
Pruebas del monitoreo post-despliegue (Sprint 3 · P3).

Ejecutar desde streamlit_demo/:
    pytest tests/test_monitoring.py -v
"""

import json
import os

import numpy as np
import pandas as pd
import pytest

from monitoring import (
    PSI_RED,
    PSI_YELLOW,
    STATUS_GREEN,
    STATUS_RED,
    STATUS_YELLOW,
    drift_report,
    needs_retraining,
    psi,
    psi_status,
    simulate_drift,
)

base_dir = os.path.join(os.path.dirname(__file__), "..")
historical = os.path.join(base_dir, "data", "historical_data.csv")


@pytest.fixture(scope="module")
def training():
    return pd.read_csv(historical)


@pytest.fixture(scope="module")
def features():
    names = []
    for model in ("delinquency", "churn"):
        with open(os.path.join(base_dir, "models", f"{model}_meta.json")) as f:
            names.extend(json.load(f)["features"])
    return list(dict.fromkeys(names))


def test_datos_iguales_dan_psi_cercano_a_cero(training):
    assert psi(training["monthly_income_cop"], training["monthly_income_cop"]) < 0.001


def test_muestra_de_la_misma_poblacion_queda_en_verde(training, features):
    batch = training.sample(1000, random_state=7)
    report = drift_report(training, batch, features)
    assert (report["status"] == STATUS_GREEN).all()


def test_datos_desplazados_dan_rojo(training):
    batch = simulate_drift(training.sample(1000, random_state=7))
    value = psi(training["monthly_income_cop"], batch["monthly_income_cop"])
    assert psi_status(value) == STATUS_RED


@pytest.mark.parametrize(
    "value, expected",
    [
        (0.0, STATUS_GREEN),
        (PSI_YELLOW - 0.001, STATUS_GREEN),
        (PSI_YELLOW, STATUS_YELLOW),
        (PSI_RED, STATUS_YELLOW),
        (PSI_RED + 0.001, STATUS_RED),
    ],
)
def test_semaforo_usa_umbrales_de_riesgo_de_credito(value, expected):
    assert psi_status(value) == expected


def test_reporte_trae_una_fila_por_variable_ordenada(training, features):
    batch = simulate_drift(training.sample(500, random_state=3))
    report = drift_report(training, batch, features)
    assert list(report.columns) == ["feature", "psi", "status"]
    assert set(report["feature"]) == set(features)
    assert report["psi"].is_monotonic_decreasing


def test_recomienda_reentrenar_solo_si_hay_rojo(training, features):
    stable = drift_report(training, training.sample(1000, random_state=11), features)
    shifted = drift_report(training, simulate_drift(training.sample(1000, random_state=11)), features)
    assert not needs_retraining(stable)
    assert needs_retraining(shifted)


def test_lote_desplazado_de_ejemplo_muestra_al_menos_una_variable_en_rojo(training, features):
    template = pd.read_csv(os.path.join(base_dir, "data", "new_clients_template.csv"))
    report = drift_report(training, simulate_drift(template), features)
    assert (report["status"] == STATUS_RED).any()


def test_variable_constante_no_rompe_el_calculo():
    constant = pd.Series(np.ones(100))
    assert psi(constant, constant) == pytest.approx(0.0)


def test_simular_desplazamiento_no_modifica_el_original(training):
    batch = training.head(20).copy()
    before = batch.copy()
    simulate_drift(batch)
    pd.testing.assert_frame_equal(batch, before)
