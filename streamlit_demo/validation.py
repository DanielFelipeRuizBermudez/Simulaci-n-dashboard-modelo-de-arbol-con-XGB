"""
Calidad de datos (DataOps) para el modelo de mora temprana.
Tarea 2 · Sprint 1 · Data Transformation and Cleaning (Delinquency).
Reglas de negocio: streamlit_demo/docs/reglas_validacion_delinquency.md

- validate_delinquency_data(df): recorre las reglas y devuelve la lista de
  errores encontrados (lista vacía = datos válidos). No modifica df.
- assert_valid_delinquency(df): lanza DataValidationError si hay errores,
  para que los datos inválidos no lleguen al modelo.
- clean_delinquency_data(df): limpieza segura antes de validar.
- transform_delinquency_features(df): variables derivadas del historial de pago.
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
