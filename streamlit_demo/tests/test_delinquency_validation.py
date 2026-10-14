"""
Quality checks automáticos (TDD) para los datos del modelo de mora.
Tarea 2 · Sprint 1 · Data Transformation and Cleaning (Delinquency).
Reglas: streamlit_demo/docs/reglas_validacion_delinquency.md

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import os

import numpy as np
import pandas as pd
import pytest

from validation import (
    DataValidationError,
    assert_valid_delinquency,
    clean_delinquency_data,
    validate_delinquency_data,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture
def valid_df():
    """Muestra mínima y válida con todas las columnas del modelo de mora."""
    return pd.DataFrame({
        "client_id": ["CL1", "CL2", "CL3"],
        "monthly_income_cop": [2_000_000.0, 3_000_000.0, 1_000_000.0],
        "credit_exposure_cop": [4_000_000.0, 1_500_000.0, 9_000_000.0],
        "avg_days_late_last_year": [0.0, 12.5, 45.0],
        "num_active_products": [1, 3, 5],
        "credit_utilization": [0.10, 0.55, 0.99],
        "months_with_bank": [6, 48, 120],
        "defaulted_30_60_days": [0, 0, 1],
    })


# --- (1) Rechaza nulos en variable obligatoria (R1) -------------------------
def test_rechaza_nulo_en_variable_obligatoria(valid_df):
    valid_df.loc[1, "monthly_income_cop"] = np.nan
    errors = validate_delinquency_data(valid_df)
    assert any("monthly_income_cop" in e and "nulos" in e for e in errors)


# --- (2) Rechaza score fuera de [0, 1] (R2) ---------------------------------
@pytest.mark.parametrize("bad_value", [-0.01, 1.5])
def test_rechaza_score_fuera_de_rango(valid_df, bad_value):
    valid_df.loc[0, "credit_utilization"] = bad_value
    errors = validate_delinquency_data(valid_df)
    assert any("credit_utilization" in e and "rango" in e for e in errors)


# --- (3) Acepta un dataset válido -------------------------------------------
def test_acepta_dataset_valido(valid_df):
    assert validate_delinquency_data(valid_df) == []


def test_acepta_historico_real_de_la_demo():
    df = pd.read_csv(os.path.join(DATA_DIR, "historical_data.csv"))
    assert validate_delinquency_data(df) == []


def test_acepta_clientes_nuevos_sin_target():
    df = pd.read_csv(os.path.join(DATA_DIR, "new_clients_template.csv"))
    assert validate_delinquency_data(df, require_target=False) == []


# --- Reglas adicionales (R3–R6) ---------------------------------------------
def test_rechaza_montos_negativos(valid_df):
    valid_df.loc[0, "credit_exposure_cop"] = -10
    errors = validate_delinquency_data(valid_df)
    assert any("credit_exposure_cop" in e for e in errors)


def test_rechaza_client_id_duplicado(valid_df):
    valid_df.loc[2, "client_id"] = "CL1"
    errors = validate_delinquency_data(valid_df)
    assert any("duplicad" in e for e in errors)


def test_rechaza_target_no_binario(valid_df):
    valid_df.loc[0, "defaulted_30_60_days"] = 2
    errors = validate_delinquency_data(valid_df)
    assert any("defaulted_30_60_days" in e for e in errors)


def test_rechaza_columna_faltante(valid_df):
    errors = validate_delinquency_data(valid_df.drop(columns=["credit_utilization"]))
    assert any("faltan columnas" in e for e in errors)


def test_bloquea_datos_invalidos(valid_df):
    valid_df.loc[0, "credit_utilization"] = 3.0
    with pytest.raises(DataValidationError):
        assert_valid_delinquency(valid_df)


# --- Limpieza -----------------------------------------------------------------
def test_limpieza_normaliza_ids_y_quita_duplicados_exactos(valid_df):
    dirty = pd.concat([valid_df, valid_df.iloc[[0]]], ignore_index=True)
    dirty.loc[1, "client_id"] = "  cl2 "
    clean = clean_delinquency_data(dirty)
    assert clean["client_id"].tolist() == ["CL1", "CL2", "CL3"]
    assert validate_delinquency_data(clean) == []
