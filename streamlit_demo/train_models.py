"""
Trains the two XGBoost models (delinquency and churn) from the SAME
historical customer base — each model just picks its own response
variable and feature subset. Runs a small hyperparameter grid search for
each model, evaluating every combination by the metric that matters
(F2 for delinquency, F1 for churn) at its best decision threshold —
never by accuracy, since both targets are imbalanced.

Run this once (after generate_data.py) with:
    python train_models.py
"""

import itertools
import json
import os

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import precision_recall_curve
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

BASE_DIR = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
os.makedirs(MODEL_DIR, exist_ok=True)

DELINQUENCY_FEATURES = [
    "monthly_income_cop", "credit_exposure_cop", "avg_days_late_last_year",
    "num_active_products", "credit_utilization", "months_with_bank",
]
CHURN_FEATURES = [
    "months_with_bank", "product_usage_score", "competitor_rate_inquiries",
    "complaint_count_last_year", "active_products_change_6m", "client_value_score",
]

# Small, fast grid — good enough for a demo without taking forever to run.
PARAM_GRID = {
    "max_depth": [3, 4, 6],
    "learning_rate": [0.05, 0.1],
    "n_estimators": [150, 300],
}


def find_best_threshold(y_true, y_proba, metric="f2"):
    """
    Finds the decision threshold that maximizes F2 (delinquency) or F1
    (churn) on a validation set — this is the standard "threshold moving"
    technique for imbalanced classification, and it's what makes the
    0.5-by-default cutoff actually meaningful for this problem.

    Uses sklearn's precision_recall_curve to get every threshold where the
    ranking of predictions actually changes (instead of an arbitrary fixed
    step size), then computes F-beta directly from precision and recall at
    each one — this is exact and fast, no need to re-run predict() in a loop.
    """
    beta = 2 if metric == "f2" else 1
    precision, recall, thresholds = precision_recall_curve(y_true, y_proba)
    # precision_recall_curve returns one more point than thresholds (for
    # recall=0), so we drop the last precision/recall value to align shapes.
    precision, recall = precision[:-1], recall[:-1]

    with np.errstate(divide="ignore", invalid="ignore"):
        fbeta = (1 + beta**2) * precision * recall / (beta**2 * precision + recall)
    fbeta = np.nan_to_num(fbeta)

    best_idx = np.argmax(fbeta)
    return float(thresholds[best_idx]), float(fbeta[best_idx])


def grid_search_train(X_train, y_train, X_val, y_val, metric):
    """
    Tries every combination in PARAM_GRID (plus scale_pos_weight, computed
    from the class imbalance of the training set) and keeps the model +
    threshold combo with the best F2/F1 score on the validation set.
    """
    neg, pos = (y_train == 0).sum(), (y_train == 1).sum()
    imbalance_ratio = neg / pos  # standard XGBoost recipe for imbalanced classes
    scale_pos_weight_options = [1, round(imbalance_ratio, 2)]

    best = {"score": -1}
    combos = list(itertools.product(
        PARAM_GRID["max_depth"], PARAM_GRID["learning_rate"],
        PARAM_GRID["n_estimators"], scale_pos_weight_options,
    ))
    print(f"  Trying {len(combos)} hyperparameter combinations...")

    for max_depth, lr, n_estimators, spw in combos:
        model = XGBClassifier(
            max_depth=max_depth, learning_rate=lr, n_estimators=n_estimators,
            scale_pos_weight=spw, eval_metric="logloss", random_state=42,
        )
        model.fit(X_train, y_train)
        proba_val = model.predict_proba(X_val)[:, 1]
        threshold, score = find_best_threshold(y_val, proba_val, metric=metric)

        if score > best["score"]:
            best = {
                "model": model, "score": score, "threshold": threshold,
                "params": {
                    "max_depth": max_depth, "learning_rate": lr,
                    "n_estimators": n_estimators, "scale_pos_weight": spw,
                },
            }

    return best


def train_model(name, target_col, features, metric):
    df = pd.read_csv(os.path.join(DATA_DIR, "historical_data.csv"))
    X = df[features]
    y = df[target_col]

    X_train, X_val, y_train, y_val = train_test_split(
        X, y, test_size=0.2, stratify=y, random_state=42
    )

    print(f"[{name}] target={target_col}  imbalance={y.mean():.1%} positive class")
    best = grid_search_train(X_train, y_train, X_val, y_val, metric=metric)

    joblib.dump(best["model"], os.path.join(MODEL_DIR, f"{name}_model.pkl"))
    with open(os.path.join(MODEL_DIR, f"{name}_meta.json"), "w") as f:
        json.dump({
            "features": features,
            "target": target_col,
            "horizon": "30/60 days" if name == "delinquency" else "3 months",
            "threshold": best["threshold"],
            f"{metric}_score": round(float(best["score"]), 4),
            "best_params": best["params"],
            "amount_column": "credit_exposure_cop" if name == "delinquency" else "client_value_score",
        }, f, indent=2)

    print(f"[{name}] best params={best['params']}")
    print(f"[{name}] threshold={best['threshold']:.2f}  {metric.upper()}-score={best['score']:.4f}")


if __name__ == "__main__":
    train_model("delinquency", "defaulted_30_60_days", DELINQUENCY_FEATURES, metric="f2")
    train_model("churn", "churned_3_months", CHURN_FEATURES, metric="f1")
    print("Models saved to:", MODEL_DIR)
