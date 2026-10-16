"""
Validación de los modelos con datos históricos.
Sprint 2 · Tareas 4 y 5 · Predictive Model (Delinquency) y Predictive Model (Churn).

Evalúa los modelos ya entrenados (models/*.pkl) sobre el mismo conjunto de
validación que se usó al entrenarlos (80/20 estratificado, random_state=42) y
guarda un reporte en reports/validation_report_<modelo>.json con:

- métrica principal en el umbral del modelo (F2 para mora, F1 para churn),
  precisión, recall y matriz de confusión;
- las variables más influyentes según SHAP (contribuciones de XGBoost);
- una comparación con las variables derivadas de las Tareas 2 y 3, entrenando
  una versión alterna solo para medir (el modelo de la app no se reemplaza).

Los datos pasan primero por las reglas de calidad de validation.py.

Uso, desde streamlit_demo/:
    python evaluate_models.py delinquency
    python evaluate_models.py churn
"""

import json
import os
import sys
import warnings

import joblib
import numpy as np
import xgboost as xgb
from sklearn.metrics import confusion_matrix, fbeta_score, precision_score, recall_score
from sklearn.model_selection import train_test_split

from train_models import (
    CHURN_FEATURES,
    DATA_DIR,
    DELINQUENCY_FEATURES,
    MODEL_DIR,
    find_best_threshold,
    load_training_data,
)
from validation import transform_churn_features, transform_delinquency_features

BASE_DIR = os.path.dirname(__file__)
REPORT_DIR = os.path.join(BASE_DIR, "reports")

MODELS = {
    "delinquency": {
        "target": "defaulted_30_60_days",
        "features": DELINQUENCY_FEATURES,
        "metric": "f2",
        "transform": transform_delinquency_features,
        "derived": ["debt_to_income_ratio", "late_over_30_days"],
    },
    "churn": {
        "target": "churned_3_months",
        "features": CHURN_FEATURES,
        "metric": "f1",
        "transform": transform_churn_features,
        "derived": ["complaints_per_month", "products_declining"],
    },
}


def load_model(name, model_dir=MODEL_DIR):
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        model = joblib.load(os.path.join(model_dir, f"{name}_model.pkl"))
    with open(os.path.join(model_dir, f"{name}_meta.json")) as f:
        meta = json.load(f)
    return model, meta


def split_data(df, target):
    """Mismo corte de validación que train_models.py."""
    return train_test_split(df, df[target], test_size=0.2, stratify=df[target], random_state=42)


def classification_metrics(y_true, y_proba, threshold, beta):
    y_pred = (y_proba >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    return {
        "score": round(float(fbeta_score(y_true, y_pred, beta=beta, zero_division=0)), 4),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "confusion_matrix": {"tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp)},
    }


def top_features_shap(model, X, n=5):
    """Promedio del |SHAP| por variable, calculado con las contribuciones de XGBoost."""
    contribs = model.get_booster().predict(xgb.DMatrix(X), pred_contribs=True)[:, :-1]
    importance = np.abs(contribs).mean(axis=0)
    order = np.argsort(importance)[::-1][:n]
    return [{"variable": X.columns[i], "mean_abs_shap": round(float(importance[i]), 4)} for i in order]


def compare_with_derived_features(name, train_df, val_df, meta):
    cfg = MODELS[name]
    beta = 2 if cfg["metric"] == "f2" else 1
    features = cfg["features"] + cfg["derived"]
    X_train = cfg["transform"](train_df)[features]
    X_val = cfg["transform"](val_df)[features]
    alt = xgb.XGBClassifier(**meta["best_params"], eval_metric="logloss", random_state=42)
    alt.fit(X_train, train_df[cfg["target"]])
    proba = alt.predict_proba(X_val)[:, 1]
    threshold, _ = find_best_threshold(val_df[cfg["target"]], proba, metric=cfg["metric"])
    result = classification_metrics(val_df[cfg["target"]], proba, threshold, beta)
    result["threshold"] = round(threshold, 4)
    result["features_added"] = cfg["derived"]
    return result


def evaluate_model(name, data_dir=DATA_DIR, model_dir=MODEL_DIR, compare_derived=True):
    cfg = MODELS[name]
    beta = 2 if cfg["metric"] == "f2" else 1

    df = load_training_data(name, data_dir=data_dir)
    train_df, val_df, _, y_val = split_data(df, cfg["target"])

    model, meta = load_model(name, model_dir=model_dir)
    X_val = val_df[cfg["features"]]
    proba = model.predict_proba(X_val)[:, 1]
    threshold = float(meta["threshold"])

    report = {
        "model": name,
        "target": cfg["target"],
        "metric": cfg["metric"],
        "threshold": round(threshold, 4),
        "n_validation": int(len(val_df)),
        "positive_rate_validation": round(float(y_val.mean()), 4),
        "best_params": meta["best_params"],
        **classification_metrics(y_val, proba, threshold, beta),
        "top_features_shap": top_features_shap(model, X_val),
    }
    if compare_derived:
        report["derived_features_comparison"] = compare_with_derived_features(name, train_df, val_df, meta)
    return report


def write_report(name, report_dir=REPORT_DIR, **kwargs):
    report = evaluate_model(name, **kwargs)
    os.makedirs(report_dir, exist_ok=True)
    path = os.path.join(report_dir, f"validation_report_{name}.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    return path, report


if __name__ == "__main__":
    names = sys.argv[1:] or list(MODELS)
    for name in names:
        path, report = write_report(name)
        metric = report["metric"].upper()
        print(f"[{name}] {metric} = {report['score']}  (umbral {report['threshold']})")
        comp = report["derived_features_comparison"]
        print(f"[{name}] con variables derivadas: {metric} = {comp['score']}")
        print(f"[{name}] reporte guardado en {path}")
