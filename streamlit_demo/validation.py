"""
Calidad de datos (DataOps) para los modelos de mora temprana y churn.
Sprint 1 · Tareas 2 y 3 · Data Transformation and Cleaning.
Reglas de negocio: streamlit_demo/docs/reglas_validacion_delinquency.md
                   streamlit_demo/docs/reglas_validacion_churn.md

- validate_delinquency_data(df): recorre las reglas y devuelve la lista de
  errores encontrados (lista vacía = datos válidos). No modifica df.
- assert_valid_delinquency(df): lanza DataValidationError si hay errores,
  para que los datos inválidos no lleguen al modelo.
- clean_delinquency_data(df): limpieza segura antes de validar.
- transform_delinquency_features(df): variables derivadas del historial de pago.
- validate_churn_data / assert_valid_churn / transform_churn_features: lo mismo
  para churn (Tarea 3).
"""

import pandas as pd

ID_COLUMN = "client_id"
DELINQUENCY_TARGET = "defaulted_30_60_days"

# R3/R4: rango permitido por variable del modelo (mínimo, máximo); None = sin límite.
DELINQUENCY_RANGES = {
    "monthly_income_cop": (0, None),
    "credit_exposure_cop": (0, None),
    "avg_days_late_last_year": (0, 365),
    "num_active_products": (0, None),
    "credit_utilization": (0, 1),  # R2: score en [0, 1]
    "months_with_bank": (0, None),
}


class DataValidationError(ValueError):
    """Los datos no cumplen las reglas de calidad y no deben llegar al modelo."""


def validate_delinquency_data(df, require_target=True):
    errors = []

    required = [ID_COLUMN] + list(DELINQUENCY_RANGES)
    if require_target:
        required.append(DELINQUENCY_TARGET)

    missing = [c for c in required if c not in df.columns]
    if missing:
        return [f"faltan columnas: {missing}"]

    # R1: nulos
    for col in required:
        n_null = int(df[col].isna().sum())
        if n_null:
            errors.append(f"{col}: {n_null} valores nulos")

    # R2, R3, R4: formato numérico y rangos
    for col, (low, high) in DELINQUENCY_RANGES.items():
        values = pd.to_numeric(df[col], errors="coerce")
        n_not_numeric = int(values.isna().sum() - df[col].isna().sum())
        if n_not_numeric:
            errors.append(f"{col}: {n_not_numeric} valores no numéricos")
        out = pd.Series(False, index=df.index)
        if low is not None:
            out |= values < low
        if high is not None:
            out |= values > high
        if out.any():
            errors.append(f"{col}: {int(out.sum())} valores fuera de rango [{low}, {high}]")

    # R5: duplicados
    n_dup = int(df[ID_COLUMN].duplicated().sum())
    if n_dup:
        errors.append(f"{ID_COLUMN}: {n_dup} ids duplicados")

    # R6: target binario
    if require_target:
        bad = ~df[DELINQUENCY_TARGET].isin([0, 1])
        if bad.any():
            errors.append(f"{DELINQUENCY_TARGET}: {int(bad.sum())} valores distintos de 0/1")

    return errors


def assert_valid_delinquency(df, require_target=True):
    errors = validate_delinquency_data(df, require_target=require_target)
    if errors:
        raise DataValidationError("Datos de mora inválidos:\n- " + "\n- ".join(errors))
    return df


def clean_delinquency_data(df):
    out = df.copy()
    out[ID_COLUMN] = out[ID_COLUMN].astype(str).str.strip().str.upper()
    return out.drop_duplicates().reset_index(drop=True)


def transform_delinquency_features(df):
    """Agrega variables derivadas del historial de pago (devuelve una copia)."""
    out = df.copy()
    # Razón deuda/ingreso: cuántos meses de ingreso representa la exposición.
    out["debt_to_income_ratio"] = (
        out["credit_exposure_cop"] / out["monthly_income_cop"]
    ).round(4)
    # Historial de mora: 1 si el promedio de días de atraso es de 30 o más.
    out["late_over_30_days"] = (out["avg_days_late_last_year"] >= 30).astype(int)
    return out


# =============================================================================
# Churn · Tarea 3 · Sprint 1 · Data Transformation and Cleaning (Churn)
# Reglas de negocio: streamlit_demo/docs/reglas_validacion_churn.md
# =============================================================================

CHURN_TARGET = "churned_3_months"

CHURN_RANGES = {
    "months_with_bank": (0, None),            # R2: antigüedad >= 0
    "product_usage_score": (0, 1),            # R3: score en [0, 1]
    "competitor_rate_inquiries": (0, None),   # R4
    "complaint_count_last_year": (0, None),   # R4
    "active_products_change_6m": (None, None),  # puede ser negativo
    "client_value_score": (0, 1),             # R3: score en [0, 1]
}


def validate_churn_data(df, require_target=True):
    errors = []

    required = [ID_COLUMN] + list(CHURN_RANGES)
    if require_target:
        required.append(CHURN_TARGET)

    missing = [c for c in required if c not in df.columns]
    if missing:
        return [f"faltan columnas: {missing}"]

    # R1: nulos
    for col in required:
        n_null = int(df[col].isna().sum())
        if n_null:
            errors.append(f"{col}: {n_null} valores nulos")

    # R2, R3, R4, R5: formato numérico y rangos
    for col, (low, high) in CHURN_RANGES.items():
        values = pd.to_numeric(df[col], errors="coerce")
        n_not_numeric = int(values.isna().sum() - df[col].isna().sum())
        if n_not_numeric:
            errors.append(f"{col}: {n_not_numeric} valores no numéricos")
        out = pd.Series(False, index=df.index)
        if low is not None:
            out |= values < low
        if high is not None:
            out |= values > high
        if out.any():
            errors.append(f"{col}: {int(out.sum())} valores fuera de rango [{low}, {high}]")

    # R6: duplicados
    n_dup = int(df[ID_COLUMN].duplicated().sum())
    if n_dup:
        errors.append(f"{ID_COLUMN}: {n_dup} ids duplicados")

    # R7: target binario
    if require_target:
        bad = ~df[CHURN_TARGET].isin([0, 1])
        if bad.any():
            errors.append(f"{CHURN_TARGET}: {int(bad.sum())} valores distintos de 0/1")

    return errors


def assert_valid_churn(df, require_target=True):
    errors = validate_churn_data(df, require_target=require_target)
    if errors:
        raise DataValidationError("Datos de churn inválidos:\n- " + "\n- ".join(errors))
    return df


def transform_churn_features(df):
    """Agrega variables derivadas de uso de producto y quejas (devuelve una copia)."""
    out = df.copy()
    # Quejas por mes de antigüedad (mínimo 1 mes para no dividir por cero).
    tenure = out["months_with_bank"].clip(lower=1)
    out["complaints_per_month"] = (out["complaint_count_last_year"] / tenure).round(4)
    # Uso de producto: 1 si el cliente cerró productos en los últimos 6 meses.
    out["products_declining"] = (out["active_products_change_6m"] < 0).astype(int)
    return out
