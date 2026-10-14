"""
Calidad de datos (DataOps) para los modelos de mora temprana y churn.
Sprint 1 · Tareas 2 y 3 · Data Transformation and Cleaning.
Reglas de negocio: streamlit_demo/docs/reglas_validacion_delinquency.md
                   streamlit_demo/docs/reglas_validacion_churn.md

Diseño (refactor XP 04, Tarea 3): las reglas de cada modelo se declaran como
un ESQUEMA (columnas obligatorias, rangos y target) y una sola función,
validate_data(df, schema), las aplica. Agregar un modelo nuevo = declarar su
esquema, sin copiar código.

API pública (la misma que antes del refactor, los tests no cambian):
- validate_delinquency_data / assert_valid_delinquency / clean_delinquency_data
- transform_delinquency_features
- validate_churn_data / assert_valid_churn / transform_churn_features
"""

import pandas as pd

ID_COLUMN = "client_id"


class DataValidationError(ValueError):
    """Los datos no cumplen las reglas de calidad y no deben llegar al modelo."""


# --- Esquemas: rango permitido por variable (mínimo, máximo); None = sin límite
DELINQUENCY_SCHEMA = {
    "name": "mora",
    "target": "defaulted_30_60_days",
    "ranges": {
        "monthly_income_cop": (0, None),
        "credit_exposure_cop": (0, None),
        "avg_days_late_last_year": (0, 365),
        "num_active_products": (0, None),
        "credit_utilization": (0, 1),
        "months_with_bank": (0, None),
    },
}

CHURN_SCHEMA = {
    "name": "churn",
    "target": "churned_3_months",
    "ranges": {
        "months_with_bank": (0, None),
        "product_usage_score": (0, 1),
        "competitor_rate_inquiries": (0, None),
        "complaint_count_last_year": (0, None),
        "active_products_change_6m": (None, None),  # puede ser negativo
        "client_value_score": (0, 1),
    },
}


# --- Motor genérico de validación -------------------------------------------
def _out_of_range(values, low, high):
    out = pd.Series(False, index=values.index)
    if low is not None:
        out |= values < low
    if high is not None:
        out |= values > high
    return out


def validate_data(df, schema, require_target=True):
    """Aplica las reglas del esquema y devuelve la lista de errores (vacía = válido)."""
    target, ranges = schema["target"], schema["ranges"]
    required = [ID_COLUMN] + list(ranges) + ([target] if require_target else [])

    missing = [c for c in required if c not in df.columns]
    if missing:
        return [f"faltan columnas: {missing}"]

    errors = []
    for col in required:  # nulos
        n_null = int(df[col].isna().sum())
        if n_null:
            errors.append(f"{col}: {n_null} valores nulos")

    for col, (low, high) in ranges.items():  # formato numérico y rangos
        values = pd.to_numeric(df[col], errors="coerce")
        n_not_numeric = int(values.isna().sum() - df[col].isna().sum())
        if n_not_numeric:
            errors.append(f"{col}: {n_not_numeric} valores no numéricos")
        n_out = int(_out_of_range(values, low, high).sum())
        if n_out:
            errors.append(f"{col}: {n_out} valores fuera de rango [{low}, {high}]")

    n_dup = int(df[ID_COLUMN].duplicated().sum())  # duplicados
    if n_dup:
        errors.append(f"{ID_COLUMN}: {n_dup} ids duplicados")

    if require_target:  # target binario
        bad = ~df[target].isin([0, 1])
        if bad.any():
            errors.append(f"{target}: {int(bad.sum())} valores distintos de 0/1")

    return errors


def assert_valid(df, schema, require_target=True):
    errors = validate_data(df, schema, require_target=require_target)
    if errors:
        raise DataValidationError(
            f"Datos de {schema['name']} inválidos:\n- " + "\n- ".join(errors)
        )
    return df


def clean_data(df):
    """Limpieza segura: normaliza client_id y quita filas duplicadas exactas."""
    out = df.copy()
    out[ID_COLUMN] = out[ID_COLUMN].astype(str).str.strip().str.upper()
    return out.drop_duplicates().reset_index(drop=True)


# --- Mora (Tarea 2) ------------------------------------------------------------
def validate_delinquency_data(df, require_target=True):
    return validate_data(df, DELINQUENCY_SCHEMA, require_target)


def assert_valid_delinquency(df, require_target=True):
    return assert_valid(df, DELINQUENCY_SCHEMA, require_target)


clean_delinquency_data = clean_data


def transform_delinquency_features(df):
    """Agrega variables derivadas del historial de pago (devuelve una copia)."""
    out = df.copy()
    out["debt_to_income_ratio"] = (
        out["credit_exposure_cop"] / out["monthly_income_cop"]
    ).round(4)
    out["late_over_30_days"] = (out["avg_days_late_last_year"] >= 30).astype(int)
    return out


# --- Churn (Tarea 3) -----------------------------------------------------------
def validate_churn_data(df, require_target=True):
    return validate_data(df, CHURN_SCHEMA, require_target)


def assert_valid_churn(df, require_target=True):
    return assert_valid(df, CHURN_SCHEMA, require_target)


def transform_churn_features(df):
    """Agrega variables derivadas de uso de producto y quejas (devuelve una copia)."""
    out = df.copy()
    tenure = out["months_with_bank"].clip(lower=1)  # mínimo 1 mes
    out["complaints_per_month"] = (out["complaint_count_last_year"] / tenure).round(4)
    out["products_declining"] = (out["active_products_change_6m"] < 0).astype(int)
    return out
