"""
El entrenamiento se bloquea si los datos no pasan las reglas de calidad.
Tarea 3 · Sprint 1 · Subtarea "Bloquear datos inválidos antes del modelo".

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import os

import pandas as pd
import pytest

from train_models import load_training_data
from validation import DataValidationError

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture
def historical():
    return pd.read_csv(os.path.join(DATA_DIR, "historical_data.csv"))


@pytest.mark.parametrize("name", ["delinquency", "churn"])
def test_datos_validos_se_cargan_para_entrenar(name):
    df = load_training_data(name, data_dir=DATA_DIR)
    assert len(df) > 0


def test_bloquea_entrenamiento_de_mora_con_datos_invalidos(historical, tmp_path):
    historical.loc[0, "credit_utilization"] = 1.7
    historical.to_csv(tmp_path / "historical_data.csv", index=False)
    with pytest.raises(DataValidationError):
        load_training_data("delinquency", data_dir=str(tmp_path))


def test_bloquea_entrenamiento_de_churn_con_datos_invalidos(historical, tmp_path):
    historical.loc[0, "churned_3_months"] = None
    historical.to_csv(tmp_path / "historical_data.csv", index=False)
    with pytest.raises(DataValidationError):
        load_training_data("churn", data_dir=str(tmp_path))
