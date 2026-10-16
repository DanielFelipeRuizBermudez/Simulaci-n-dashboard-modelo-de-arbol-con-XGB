"""
Evaluación del modelo de churn con F1 en el conjunto de validación.
Tarea 5 · Sprint 2 · Predictive Model (Churn).

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import json
import os

import pytest

from evaluate_models import evaluate_model, load_model
from train_models import CHURN_FEATURES

REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "validation_report_churn.json")


@pytest.fixture(scope="module")
def report():
    return evaluate_model("churn", compare_derived=False)


def test_f1_en_rango(report):
    assert report["metric"] == "f1"
    assert 0 <= report["score"] <= 1


def test_matriz_de_confusion_cubre_todo_el_conjunto_de_validacion(report):
    assert sum(report["confusion_matrix"].values()) == report["n_validation"]


def test_f1_coincide_con_el_entrenamiento(report):
    _, meta = load_model("churn")
    assert report["score"] == pytest.approx(meta["f1_score"], abs=0.01)


def test_no_marca_a_todos_los_clientes_como_fuga(report):
    assert report["confusion_matrix"]["tn"] > 0


def test_top5_variables_shap_son_del_modelo(report):
    top = [item["variable"] for item in report["top_features_shap"]]
    assert len(top) == 5
    assert set(top) <= set(CHURN_FEATURES)


def test_reporte_guardado_en_el_repo():
    with open(REPORT_PATH, encoding="utf-8") as f:
        saved = json.load(f)
    assert saved["metric"] == "f1"
    assert 0 <= saved["score"] <= 1
    assert saved["derived_features_comparison"]["features_added"] == [
        "complaints_per_month",
        "products_declining",
    ]
