"""
Validación del modelo de mora con datos históricos.
Tarea 4 · Sprint 2 · Predictive Model (Delinquency).

Ejecutar desde streamlit_demo/:
    pytest -v
"""

import json
import os

import pytest

from evaluate_models import evaluate_model, load_model, write_report
from train_models import DELINQUENCY_FEATURES

REPORT_PATH = os.path.join(os.path.dirname(__file__), "..", "reports", "validation_report_delinquency.json")


@pytest.fixture(scope="module")
def report():
    return evaluate_model("delinquency", compare_derived=False)


def test_metricas_en_rango(report):
    assert report["metric"] == "f2"
    for key in ["score", "precision", "recall"]:
        assert 0 <= report[key] <= 1


def test_matriz_de_confusion_cubre_todo_el_conjunto_de_validacion(report):
    assert sum(report["confusion_matrix"].values()) == report["n_validation"]


def test_usa_el_umbral_del_modelo(report):
    _, meta = load_model("delinquency")
    assert report["threshold"] == round(meta["threshold"], 4)


def test_f2_coincide_con_el_entrenamiento(report):
    _, meta = load_model("delinquency")
    assert report["score"] == pytest.approx(meta["f2_score"], abs=0.01)


def test_top5_variables_shap_son_del_modelo(report):
    top = [item["variable"] for item in report["top_features_shap"]]
    assert len(top) == 5
    assert set(top) <= set(DELINQUENCY_FEATURES)


def test_comparacion_con_variables_derivadas():
    comp = evaluate_model("delinquency")["derived_features_comparison"]
    assert comp["features_added"] == ["debt_to_income_ratio", "late_over_30_days"]
    assert 0 <= comp["score"] <= 1


def test_write_report_guarda_el_json(tmp_path):
    path, _ = write_report("delinquency", report_dir=str(tmp_path), compare_derived=False)
    with open(path, encoding="utf-8") as f:
        assert json.load(f)["model"] == "delinquency"


def test_reporte_guardado_en_el_repo():
    with open(REPORT_PATH, encoding="utf-8") as f:
        saved = json.load(f)
    assert saved["metric"] == "f2"
    assert 0 <= saved["score"] <= 1
