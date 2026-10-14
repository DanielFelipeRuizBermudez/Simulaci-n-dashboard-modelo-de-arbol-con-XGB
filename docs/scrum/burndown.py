"""
Genera el gráfico de Burndown de cada Sprint a partir de docs/scrum/burndown.csv.

Uso (desde la raíz del repo):
    pip install matplotlib
    python docs/scrum/burndown.py

Columnas del CSV: sprint, dia, fecha, ideal, real (puntos restantes al final del día).
Para el Sprint 2 basta con agregar sus filas al CSV y volver a correr el script.
"""

import csv
import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(HERE, "..", "evidencias")


def load_rows(path=os.path.join(HERE, "burndown.csv")):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def plot_sprint(rows, sprint):
    data = [r for r in rows if r["sprint"] == str(sprint)]
    labels = [r["fecha"] for r in data]
    ideal = [float(r["ideal"]) for r in data]
    real = [float(r["real"]) if r["real"] != "" else None for r in data]
    x = range(len(data))

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.plot(x, ideal, linestyle="--", color="#8a8a8a", marker="o", label="Ideal (plan)")
    xs = [i for i, v in zip(x, real) if v is not None]
    ys = [v for v in real if v is not None]
    ax.plot(xs, ys, color="#0a8f65", marker="o", linewidth=2.5, label="Real")
    for i, v in zip(xs, ys):
        ax.annotate(f"{v:.0f}", (i, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=9)
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels)
    ax.set_ylim(bottom=0, top=max(ideal + ys) * 1.15)
    ax.set_ylabel("Puntos restantes")
    ax.set_title(f"Burndown · Sprint {sprint}")
    ax.grid(axis="y", alpha=0.3)
    ax.legend(loc="lower left")
    fig.tight_layout()
    os.makedirs(OUT_DIR, exist_ok=True)
    path = os.path.join(OUT_DIR, f"burndown_sprint{sprint}.png")
    fig.savefig(path, dpi=150)
    plt.close(fig)
    return path


if __name__ == "__main__":
    rows = load_rows()
    for sprint in sorted({r["sprint"] for r in rows}):
        print("Generado:", plot_sprint(rows, sprint))
