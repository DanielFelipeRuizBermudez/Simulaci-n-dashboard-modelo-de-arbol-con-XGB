"""
Quality checks automáticos (TDD) para los datos del modelo de churn.
Tarea 3 · Sprint 1 · Data Transformation and Cleaning (Churn).
Reglas: streamlit_demo/docs/reglas_validacion_churn.md

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import os

import numpy as np
import pandas as pd
import pytest

from validation import (
    DataValidationError,
    assert_valid_churn,
    transform_churn_features,
    validate_churn_data,
)

DATA_DIR = os.path.join(os.path.dirname(__file__), "..", "data")


@pytest.fixture
def valid_df():
    """Muestra mínima y válida con todas las columnas del modelo de churn."""
    return pd.DataFrame({
        "client_id": ["CL1", "CL2", "CL3"],
        "months_with_bank": [12, 3, 0],
        "product_usage_score": [0.80, 0.25, 0.50],
        "competitor_rate_inquiries": [0, 2, 1],
        "complaint_count_last_year": [6, 3, 1],
        "active_products_change_6m": [1, -2, 0],
        "client_value_score": [0.40, 0.10, 0.90],
        "churned_3_months": [0, 1, 0],
    })


# --- (1) Rechaza registro incompleto (R1) -----------------------------------
def test_rechaza_registro_incompleto(valid_df):
    valid_df.loc[0, "product_usage_score"] = np.nan
    errors = validate_churn_data(valid_df)
    assert any("product_usage_score" in e and "nulos" in e for e in errors)


# --- (2) Rechaza duplicado (R6) ---------------------------------------------
def test_rechaza_cliente_duplicado(valid_df):
    valid_df.loc[1, "client_id"] = "CL1"
    errors = validate_churn_data(valid_df)
    assert any("duplicad" in e for e in errors)


# --- (3) Acepta dataset limpio ----------------------------------------------
def test_acepta_dataset_limpio(valid_df):
    assert validate_churn_data(valid_df) == []


def test_acepta_historico_real_de_la_demo():
    df = pd.read_csv(os.path.join(DATA_DIR, "historical_data.csv"))
    assert validate_churn_data(df) == []


def test_acepta_clientes_nuevos_sin_target():
    df = pd.read_csv(os.path.join(DATA_DIR, "new_clients_template.csv"))
    assert validate_churn_data(df, require_target=False) == []


# --- Reglas adicionales -------------------------------------------------------
def test_rechaza_antiguedad_negativa(valid_df):
    valid_df.loc[0, "months_with_bank"] = -1
    errors = validate_churn_data(valid_df)
    assert any("months_with_bank" in e for e in errors)


def test_rechaza_score_fuera_de_rango(valid_df):
    valid_df.loc[2, "client_value_score"] = 1.2
    errors = validate_churn_data(valid_df)
    assert any("client_value_score" in e and "rango" in e for e in errors)


def test_acepta_cambio_de_productos_negativo(valid_df):
    valid_df.loc[0, "active_products_change_6m"] = -3
    assert validate_churn_data(valid_df) == []


def test_rechaza_target_no_binario(valid_df):
    valid_df.loc[0, "churned_3_months"] = 3
    errors = validate_churn_data(valid_df)
    assert any("churned_3_months" in e for e in errors)


def test_bloquea_datos_invalidos(valid_df):
    valid_df.loc[0, "complaint_count_last_year"] = -5
    with pytest.raises(DataValidationError):
        assert_valid_churn(valid_df)


# --- Transformaciones (uso de producto y quejas) ------------------------------
def test_calcula_quejas_por_mes_de_antiguedad(valid_df):
    out = transform_churn_features(valid_df)
    # 6 quejas / 12 meses = 0.5 ; 3 / 3 = 1.0 ; antigüedad 0 se trata como 1 mes
    assert out["complaints_per_month"].tolist() == [0.5, 1.0, 1.0]


def test_marca_clientes_que_cierran_productos(valid_df):
    out = transform_churn_features(valid_df)
    assert out["products_declining"].tolist() == [0, 1, 0]


def test_transformacion_no_modifica_el_original(valid_df):
    transform_churn_features(valid_df)
    assert "complaints_per_month" not in valid_df.columns
