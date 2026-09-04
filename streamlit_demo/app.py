"""
FinBank Predictive Analytics Demo — FinTech Solutions
Run with: streamlit run app.py

Requires models already trained: run `python generate_data.py` then
`python train_models.py` first.

For the "Ask Sol" chat tab you need a Gemini API key (from Google AI Studio).
Set it as an environment variable GEMINI_API_KEY, or paste it in the sidebar
when the app is running.
"""

import base64
import json
import os

import joblib
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import shap
import streamlit as st

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
NEW_CLIENTS_TEMPLATE = os.path.join(DATA_DIR, "new_clients_template.csv")
LOGO_PATH = os.path.join(ASSETS_DIR, "logo.png")
SOL_MARK_PATH = os.path.join(ASSETS_DIR, "sol_mark.png")
SOL_AVATAR = SOL_MARK_PATH if os.path.exists(SOL_MARK_PATH) else ":material/wb_sunny:"

BRAND_GREEN = "#00FCA9"
BRAND_GREEN_DEEP = "#0a8f65"
BRAND_DARK = "#272727"
ALERT_RED = "#E4572E"

PLOTLY_CONFIG = {"displayModeBar": False}

st.set_page_config(
    page_title="FinBank Predictive Analytics",
    page_icon=SOL_MARK_PATH if os.path.exists(SOL_MARK_PATH) else "☀️",
    layout="wide",
)


# ---------- visual system (CSS) ----------

st.markdown(
    f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap');

    html, body, [class*="css"] {{
        font-family: 'Manrope', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }}

    .stApp {{
        background:
            radial-gradient(1100px 550px at 92% -8%, rgba(0,252,169,0.10), transparent 60%),
            radial-gradient(900px 500px at -8% 8%, rgba(0,252,169,0.06), transparent 55%),
            #FFFFFF;
    }}

    section[data-testid="stSidebar"] {{
        background: linear-gradient(180deg, #1c1c1c 0%, {BRAND_DARK} 100%);
        border-right: 1px solid rgba(0,252,169,0.15);
    }}
    section[data-testid="stSidebar"] label,
    section[data-testid="stSidebar"] p,
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3,
    section[data-testid="stSidebar"] .stMarkdown,
    section[data-testid="stSidebar"] .stCaption {{ color: #EDEDED; }}
    section[data-testid="stSidebar"] hr {{ border-color: rgba(255,255,255,0.15); }}

    /* Language toggle — scoped to its own radiogroup so it doesn't touch the
       table/charts/explain segmented control on the light background. */
    div[role="radiogroup"][aria-label="Idioma / Language"] {{
        background: rgba(255,255,255,0.07);
        border: 1px solid rgba(255,255,255,0.09);
        border-radius: 999px;
        padding: 3px;
        gap: 2px !important;
    }}
    div[role="radiogroup"][aria-label="Idioma / Language"] button[role="radio"] {{
        border: none !important;
        border-radius: 999px !important;
        background: transparent !important;
        color: #b7b7b7 !important;
        font-weight: 600;
        transition: background .15s ease, color .15s ease;
    }}
    div[role="radiogroup"][aria-label="Idioma / Language"] button[role="radio"]:hover {{
        background: rgba(255,255,255,0.08) !important;
        color: #fff !important;
    }}
    div[role="radiogroup"][aria-label="Idioma / Language"] button[role="radio"][aria-checked="true"] {{
        background: {BRAND_GREEN} !important;
        color: {BRAND_DARK} !important;
        box-shadow: 0 2px 10px rgba(0,252,169,0.35);
    }}
    div[role="radiogroup"][aria-label="Idioma / Language"] button[role="radio"][aria-checked="true"]:hover {{
        background: {BRAND_GREEN} !important;
        color: {BRAND_DARK} !important;
    }}

    .stTabs [data-baseweb="tab-list"] {{ gap: 6px; border-bottom: 1px solid rgba(39,39,39,0.08); }}
    .stTabs [data-baseweb="tab"] {{
        height: 46px; padding: 0 18px; border-radius: 10px 10px 0 0;
        font-weight: 700; color: #6b6b6b; transition: all .2s ease;
    }}
    .stTabs [aria-selected="true"] {{
        color: {BRAND_DARK} !important;
        background: rgba(0,252,169,0.12);
        border-bottom: 3px solid {BRAND_GREEN} !important;
    }}

    .stButton button, .stDownloadButton button {{
        border-radius: 10px; border: 1.5px solid {BRAND_GREEN}; font-weight: 600;
        transition: all .15s ease;
    }}
    .stButton button:hover, .stDownloadButton button:hover {{
        background: {BRAND_GREEN}; color: #10241d;
        box-shadow: 0 4px 14px rgba(0,252,169,0.35); transform: translateY(-1px);
    }}

    div[data-testid="stVerticalBlockBorderWrapper"] {{ border-radius: 16px !important; }}
    [data-testid="stDataFrame"] {{ border-radius: 12px; overflow: hidden; }}

    ::-webkit-scrollbar {{ width: 10px; height: 10px; }}
    ::-webkit-scrollbar-thumb {{ background: rgba(0,252,169,0.45); border-radius: 8px; }}
    ::-webkit-scrollbar-track {{ background: transparent; }}

    /* ---- custom components ---- */
    .ftx-hero {{
        display: flex; align-items: center; justify-content: space-between; gap: 20px; flex-wrap: wrap;
        background: linear-gradient(120deg, #ffffff 0%, #f2fffa 100%);
        border: 1px solid rgba(0,252,169,0.35);
        border-radius: 20px; padding: 20px 26px; margin-bottom: 18px;
        box-shadow: 0 10px 30px rgba(39,39,39,0.06);
    }}
    .ftx-hero-left {{ display:flex; align-items:center; gap:18px; }}
    .ftx-hero-left img {{ height: 40px; }}
    .ftx-hero h1 {{ margin:0; font-size: 1.45rem; font-weight:800; color:{BRAND_DARK}; }}
    .ftx-hero p {{ margin:2px 0 0; color:#5b5b5b; font-size:0.92rem; }}
    .ftx-status-row {{ display:flex; gap:10px; flex-wrap:wrap; }}
    .ftx-chip {{
        display:flex; align-items:center; gap:6px; background:#ffffff;
        border:1px solid rgba(39,39,39,0.08); border-radius:999px; padding:6px 12px;
        font-size:0.78rem; font-weight:600; color:{BRAND_DARK}; box-shadow:0 2px 6px rgba(39,39,39,0.05);
        white-space: nowrap;
    }}
    .ftx-dot {{ width:8px; height:8px; border-radius:50%; background:{BRAND_GREEN}; box-shadow:0 0 0 3px rgba(0,252,169,0.25); }}

    .ftx-stat-card {{
        background:#fff; border:1px solid rgba(39,39,39,0.07); border-radius:16px;
        padding:14px 16px; height:100%; transition:transform .15s ease, box-shadow .15s ease;
    }}
    .ftx-stat-card:hover {{ transform:translateY(-2px); box-shadow:0 10px 24px rgba(39,39,39,0.08); }}
    .ftx-stat-icon {{ font-size:1.25rem; }}
    .ftx-stat-label {{ font-size:0.74rem; color:#6b6b6b; font-weight:700; margin-top:6px; text-transform:uppercase; letter-spacing:.03em; }}
    .ftx-stat-value {{ font-size:1.55rem; font-weight:800; color:{BRAND_DARK}; margin-top:2px; }}
    .ftx-stat-delta {{ font-size:0.76rem; font-weight:700; margin-top:6px; display:inline-block; padding:2px 8px; border-radius:999px; }}
    .ftx-stat-delta.up {{ background:rgba(228,87,46,0.12); color:{ALERT_RED}; }}
    .ftx-stat-delta.down {{ background:rgba(0,252,169,0.18); color:{BRAND_GREEN_DEEP}; }}

    .ftx-badge {{ display:inline-flex; align-items:center; gap:6px; padding:5px 12px; border-radius:999px; font-weight:700; font-size:0.8rem; }}
    .ftx-badge.high {{ background:rgba(228,87,46,0.12); color:{ALERT_RED}; border:1px solid rgba(228,87,46,0.3); }}
    .ftx-badge.low {{ background:rgba(0,252,169,0.16); color:{BRAND_GREEN_DEEP}; border:1px solid rgba(0,252,169,0.4); }}
    .ftx-badge-dot {{ display:inline-block; width:6px; height:6px; border-radius:50%; }}
    .ftx-badge.high .ftx-badge-dot {{ background:{ALERT_RED}; }}
    .ftx-badge.low .ftx-badge-dot {{ background:{BRAND_GREEN_DEEP}; }}

    .ftx-client-header {{ display:flex; align-items:center; gap:10px; margin:6px 0 2px; flex-wrap:wrap; }}
    .ftx-client-name {{ font-weight:800; font-size:1.15rem; color:{BRAND_DARK}; }}

    .ftx-profile-grid {{ display:grid; grid-template-columns: repeat(auto-fit, minmax(160px,1fr)); gap:10px; margin:10px 0 4px; }}
    .ftx-profile-item {{ background:#fbfbfb; border:1px solid rgba(39,39,39,0.06); border-radius:12px; padding:10px 12px; }}
    .ftx-profile-item .lbl {{ font-size:0.72rem; color:#6b6b6b; font-weight:600; }}
    .ftx-profile-item .val {{ font-size:1.05rem; color:{BRAND_DARK}; font-weight:800; margin-top:2px; }}

    .ftx-call-card {{
        display:flex; align-items:center; justify-content:space-between; gap:16px; flex-wrap: wrap;
        background: linear-gradient(120deg, #171717 0%, {BRAND_DARK} 100%);
        border-radius:18px; padding:16px 22px; margin-bottom:14px;
        box-shadow: 0 12px 30px rgba(0,0,0,0.18);
    }}
    .ftx-call-left {{ display:flex; align-items:center; gap:14px; }}
    .ftx-call-avatar {{
        width:50px; height:50px; border-radius:50%; display:flex; align-items:center; justify-content:center;
        font-size:1.4rem; background:{BRAND_GREEN};
        animation: ftx-pulse 2s infinite;
    }}
    @keyframes ftx-pulse {{
        0% {{ box-shadow: 0 0 0 0 rgba(0,252,169,0.45); }}
        70% {{ box-shadow: 0 0 0 14px rgba(0,252,169,0); }}
        100% {{ box-shadow: 0 0 0 0 rgba(0,252,169,0); }}
    }}
    .ftx-call-name {{ color:#fff; font-weight:800; font-size:1.05rem; }}
    .ftx-call-sub {{ color:#b7b7b7; font-size:0.8rem; }}
    .ftx-call-status {{ display:flex; align-items:center; gap:10px; color:{BRAND_GREEN}; font-weight:700; font-size:0.85rem; }}
    .ftx-wave {{ display:flex; align-items:flex-end; gap:3px; height:18px; }}
    .ftx-wave span {{ width:3px; background:{BRAND_GREEN}; border-radius:2px; display:inline-block; animation: ftx-wave 1.1s infinite ease-in-out; }}
    .ftx-wave span:nth-child(1) {{ animation-delay:0s; }}
    .ftx-wave span:nth-child(2) {{ animation-delay:0.15s; }}
    .ftx-wave span:nth-child(3) {{ animation-delay:0.3s; }}
    .ftx-wave span:nth-child(4) {{ animation-delay:0.45s; }}
    .ftx-wave span:nth-child(5) {{ animation-delay:0.6s; }}
    @keyframes ftx-wave {{ 0%,100% {{ height:4px; }} 50% {{ height:18px; }} }}

    .ftx-footer {{ background:#fbfbfb; border:1px solid rgba(39,39,39,0.06); border-radius:12px; padding:10px 16px; color:#6b6b6b; font-size:0.8rem; }}

    .ftx-sidebar-tagline {{ text-align:center; color:#9c9c9c; font-size:0.75rem; margin-top:-4px; margin-bottom:12px; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- icon system ----------
#
# Streamlit natively renders ":material/name:" shortcodes as small mono-line
# symbols (not emoji) inside st.markdown/st.write text, button/tab/expander
# labels and chat_message avatars — used throughout below wherever those
# widgets are involved. Raw HTML blocks (unsafe_allow_html=True) don't get
# that treatment, so the hand-drawn outline icons below cover those spots
# (hero, stat cards, call card, client profile grid, footer).

ICONS = {
    "group": '<circle cx="8.5" cy="8" r="3"/><path d="M3.5 20c0-3.3 2.2-5.5 5-5.5s5 2.2 5 5.5"/>'
             '<circle cx="17" cy="9" r="2.3"/><path d="M14.8 20c0-2.6 1-4.6 3-5.4"/>',
    "flag": '<line x1="5" y1="4" x2="5" y2="21"/><path d="M5 5h11l-3 4 3 4H5z"/>',
    "bar_chart": '<rect x="4" y="12" width="4" height="8" rx="0.5"/>'
                 '<rect x="10" y="7" width="4" height="13" rx="0.5"/>'
                 '<rect x="16" y="3" width="4" height="17" rx="0.5"/>',
    "payments": '<circle cx="12" cy="12" r="8.5"/>'
                '<text x="12" y="16" font-size="10" text-anchor="middle" '
                'font-family="Manrope, sans-serif" fill="currentColor" stroke="none">$</text>',
    "diamond": '<polygon points="12,3 19,9 12,21 5,9" fill="currentColor" stroke="none"/>',
    "bank": '<polygon points="12,3 21,9 3,9"/><line x1="5" y1="9" x2="5" y2="18"/>'
            '<line x1="9" y1="9" x2="9" y2="18"/><line x1="15" y1="9" x2="15" y2="18"/>'
            '<line x1="19" y1="9" x2="19" y2="18"/><line x1="3" y1="20" x2="21" y2="20"/>',
    "clock": '<circle cx="12" cy="12" r="8.5"/><line x1="12" y1="12" x2="12" y2="7"/>'
             '<line x1="12" y1="12" x2="16" y2="14"/>',
    "package": '<rect x="4" y="7" width="16" height="13" rx="1.5"/>'
               '<line x1="4" y1="7" x2="12" y2="3"/><line x1="20" y1="7" x2="12" y2="3"/>'
               '<line x1="12" y1="7" x2="12" y2="20"/>',
    "credit_card": '<rect x="3" y="6" width="18" height="12" rx="2"/><line x1="3" y1="10" x2="21" y2="10"/>',
    "calendar": '<rect x="4" y="6" width="16" height="14" rx="1.5"/><line x1="4" y1="10" x2="20" y2="10"/>'
                '<line x1="8" y1="3" x2="8" y2="7"/><line x1="16" y1="3" x2="16" y2="7"/>',
    "trending_up": '<polyline points="4,17 10,11 14,15 20,7"/><polyline points="14,7 20,7 20,13"/>',
    "search": '<circle cx="10.5" cy="10.5" r="6.5"/><line x1="15.5" y1="15.5" x2="21" y2="21"/>',
    "campaign": '<path d="M3 10v4h3l6 4V6l-6 4H3z"/><path d="M14.5 9a4 4 0 010 6"/>',
    "sync_alt": '<polyline points="4,7 20,7"/><polyline points="16,3 20,7 16,11"/>'
                '<polyline points="20,17 4,17"/><polyline points="8,13 4,17 8,21"/>',
    "sun": '<circle cx="12" cy="12" r="4.5"/><line x1="12" y1="2" x2="12" y2="5"/>'
           '<line x1="12" y1="19" x2="12" y2="22"/><line x1="2" y1="12" x2="5" y2="12"/>'
           '<line x1="19" y1="12" x2="22" y2="12"/><line x1="4.5" y1="4.5" x2="6.6" y2="6.6"/>'
           '<line x1="17.4" y1="17.4" x2="19.5" y2="19.5"/><line x1="4.5" y1="19.5" x2="6.6" y2="17.4"/>'
           '<line x1="17.4" y1="6.6" x2="19.5" y2="4.5"/>',
    "info": '<circle cx="12" cy="12" r="9"/><line x1="12" y1="11" x2="12" y2="16"/>'
            '<circle cx="12" cy="7.6" r="1" fill="currentColor" stroke="none"/>',
    "mic": '<rect x="9" y="2" width="6" height="11" rx="3"/><path d="M5 11a7 7 0 0014 0"/>'
           '<line x1="12" y1="18" x2="12" y2="22"/><line x1="8" y1="22" x2="16" y2="22"/>',
}


def icon_svg(name, size=16, color="currentColor", stroke_width=1.8):
    body = ICONS.get(name, "")
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" '
        f'viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{stroke_width}" '
        f'stroke-linecap="round" stroke-linejoin="round" '
        f'style="display:inline-block;vertical-align:-0.15em;flex-shrink:0;">{body}</svg>'
    )


# ---------- i18n ----------
#
# The UI (labels, buttons, headers) is translated via TR below and the t()
# helper. Sol's chat is a separate matter: it already detects the language
# of each question and replies in kind (see SOL_SYSTEM_PROMPT), regardless
# of the UI language chosen here.

TR = {
    "app_title": {
        "en": "Predictive Analytics — Live Demo",
        "es": "Analítica Predictiva — Demo en Vivo",
    },
    "app_subtitle": {
        "en": "FinTech Solutions · Explainable XGBoost models for early delinquency and churn detection",
        "es": "FinTech Solutions · Modelos XGBoost explicables para detección temprana de morosidad y deserción de clientes",
    },
    "status_models_active": {"en": "Models active", "es": "Modelos activos"},
    "status_sol_ready": {"en": "Sol ready for calls", "es": "Sol lista para llamar"},
    "tab_delinquency": {"en": "Delinquency", "es": "Morosidad"},
    "tab_churn": {"en": "Churn", "es": "Deserción"},
    "tab_sol": {"en": "Ask Sol", "es": "Pregúntale a Sol"},
    "delinquency_title": {"en": "Early Delinquency Detection", "es": "Detección Temprana de Morosidad"},
    "churn_title": {"en": "Churn Risk Detection", "es": "Detección de Riesgo de Deserción"},
    "model_not_found": {
        "en": "Model not found. Run `python train_models.py` first (after `python generate_data.py`).",
        "es": "Modelo no encontrado. Corre `python train_models.py` primero (después de `python generate_data.py`).",
    },
    "about_model": {"en": ":material/info: About this model", "es": ":material/info: Sobre este modelo"},
    "about_model_body": {
        "en": (
            "Trained by FinTech Solutions on FinBank's historical customer base "
            "(same base used for both models — this one just uses `{target}` "
            "as its response variable, predicting the event within "
            "**{horizon}**). Validation {metric_name}: **{metric_value}**, "
            "with hyperparameters and decision threshold both tuned to optimize "
            "{metric_name}, not accuracy. Best hyperparameters found via grid "
            "search: `{best_params}`.\n\n"
            "Below, upload a file with **new clients** to score them instantly."
        ),
        "es": (
            "Entrenado por FinTech Solutions con la base histórica de clientes de "
            "FinBank (la misma base usada para ambos modelos — este solo usa "
            "`{target}` como variable de respuesta, prediciendo el evento dentro "
            "de **{horizon}**). {metric_name} de validación: **{metric_value}**, "
            "con hiperparámetros y umbral de decisión ajustados para optimizar "
            "{metric_name}, no precisión (accuracy). Mejores hiperparámetros "
            "encontrados vía grid search: `{best_params}`.\n\n"
            "Abajo, sube un archivo con **nuevos clientes** para calificarlos al instante."
        ),
    },
    "download_sample": {
        "en": ":material/download: Sample 'new clients' file",
        "es": ":material/download: Archivo de ejemplo de 'nuevos clientes'",
    },
    "upload_label": {"en": "Upload new client data ({label})", "es": "Subir datos de nuevos clientes ({label})"},
    "missing_columns": {
        "en": "The uploaded file is missing required columns: {missing}",
        "es": "Al archivo subido le faltan columnas requeridas: {missing}",
    },
    "clear_data": {"en": ":material/delete: Remove data", "es": ":material/delete: Quitar datos"},
    "reset_sample": {"en": ":material/restart_alt: Restore sample", "es": ":material/restart_alt: Restaurar ejemplo"},
    "toast_uploaded": {"en": "{n} clients loaded", "es": "{n} clientes cargados"},
    "toast_cleared": {"en": "Data removed", "es": "Datos eliminados"},
    "toast_reset": {"en": "Sample data restored", "es": "Datos de ejemplo restaurados"},
    "no_data_loaded": {
        "en": "No data loaded. Upload a file or restore the sample to see results.",
        "es": "No hay datos cargados. Sube un archivo o restaura el ejemplo para ver resultados.",
    },
    "key_indicators": {"en": "### Key indicators", "es": "### Indicadores clave"},
    "clients_evaluated": {"en": "Clients evaluated", "es": "Clientes evaluados"},
    "flagged_high_risk": {"en": "Flagged as high {label} risk", "es": "Marcados como alto riesgo de {label}"},
    "avg_risk_score": {"en": "Average risk score", "es": "Puntaje de riesgo promedio"},
    "exposure_at_risk": {"en": "Exposure at risk (COP)", "es": "Exposición en riesgo (COP)"},
    "client_value_at_risk": {"en": "Client value at risk", "es": "Valor de cliente en riesgo"},
    "prioritized_list": {"en": "### Prioritized client list", "es": "### Lista priorizada de clientes"},
    "risk_distribution": {"en": "### Risk score distribution", "es": "### Distribución del puntaje de riesgo"},
    "view_selector_label": {"en": "View", "es": "Vista"},
    "view_table": {"en": "Table", "es": "Tabla"},
    "view_charts": {"en": "Distribution", "es": "Distribución"},
    "view_explain": {"en": "Explainability", "es": "Explicabilidad"},
    "hist_caption": {
        "en": "How risk scores are distributed across all uploaded clients. The dashed line marks the flagging threshold.",
        "es": "Cómo se distribuye el puntaje de riesgo entre todos los clientes cargados. La línea punteada marca el umbral de marcado.",
    },
    "ranking_caption": {
        "en": "All clients ranked by risk score, colored by flag status.",
        "es": "Todos los clientes ordenados por puntaje de riesgo, coloreados según su estado.",
    },
    "threshold_label": {"en": "Threshold: {pct}", "es": "Umbral: {pct}"},
    "risk_pct_axis": {"en": "Risk score (%)", "es": "Puntaje de riesgo (%)"},
    "client_count_axis": {"en": "# clients", "es": "# clientes"},
    "col_client_id": {"en": "Client", "es": "Cliente"},
    "col_risk_score": {"en": "Risk (%)", "es": "Riesgo (%)"},
    "col_flagged": {"en": "Flagged", "es": "Marcado"},
    "global_shap_header": {
        "en": "### What drives this model overall? (global SHAP)",
        "es": "### ¿Qué impulsa este modelo en general? (SHAP global)",
    },
    "global_shap_caption": {
        "en": "Average influence of each variable across all {n} uploaded clients "
              "on being classified as high {label} risk (class 1).",
        "es": "Influencia promedio de cada variable, entre los {n} clientes cargados, "
              "en ser clasificado como alto riesgo de {label} (clase 1).",
    },
    "beeswarm_caption": {
        "en": "Each dot is one client. Position shows whether that variable pushed "
              "their score up (right) or down (left); color shows whether their "
              "own value for that variable was low or high.",
        "es": "Cada punto es un cliente. La posición muestra si esa variable subió "
              "(derecha) o bajó (izquierda) su puntaje; el color muestra si el "
              "valor de esa variable para ese cliente fue bajo o alto.",
    },
    "beeswarm_low": {"en": "Low", "es": "Bajo"},
    "beeswarm_high": {"en": "High", "es": "Alto"},
    "beeswarm_colorbar_title": {"en": "Feature value", "es": "Valor de la variable"},
    "beeswarm_hover_value": {"en": "Value", "es": "Valor"},
    "bubble_hover_impact": {"en": "Impact", "es": "Impacto"},
    "shap_value_axis": {
        "en": "Impact on the risk score (SHAP value)",
        "es": "Impacto en el puntaje de riesgo (valor SHAP)",
    },
    "local_shap_header": {
        "en": "### Why was one specific client flagged? (local SHAP)",
        "es": "### ¿Por qué se marcó a un cliente específico? (SHAP local)",
    },
    "select_client": {"en": "Select a client", "es": "Selecciona un cliente"},
    "client_risk_caption": {
        "en": "Risk score for {client}: **{score}** ({status}). "
              "Bars to the right push the score up, bars to the left push it down.",
        "es": "Puntaje de riesgo para {client}: **{score}** ({status}). "
              "Las barras a la derecha suben el puntaje, las de la izquierda lo bajan.",
    },
    "client_profile_header": {"en": "**Client snapshot**", "es": "**Ficha del cliente**"},
    "flagged_status": {"en": "flagged", "es": "marcado"},
    "not_flagged_status": {"en": "not flagged", "es": "no marcado"},
    "risk_high_badge": {"en": "High risk", "es": "Alto riesgo"},
    "risk_low_badge": {"en": "Low risk", "es": "Bajo riesgo"},
    "sol_subheader": {"en": "Ask Sol", "es": "Pregúntale a Sol"},
    "sol_caption": {
        "en": "Text version of Sol for this demo (the real product uses voice calls). "
              "Works in English or Spanish — Sol replies in whichever language you use. "
              "E.g. \"How many clients are flagged for churn?\" or "
              "\"¿Quiénes están predichos para entrar en mora?\"",
        "es": "Versión en texto de Sol para este demo (el producto real usa llamadas de voz). "
              "Funciona en inglés o español — Sol responde en el idioma que uses. "
              "Ej. \"¿Quiénes están predichos para entrar en mora?\" o "
              "\"How many clients are flagged for churn?\"",
    },
    "sol_call_status_demo": {"en": "Simulated call · text preview", "es": "Llamada simulada · vista en texto"},
    "sol_call_live": {"en": "● Online", "es": "● En línea"},
    "sol_status_thinking": {
        "en": ":material/psychology: Sol is processing your question…",
        "es": ":material/psychology: Sol está procesando tu pregunta…",
    },
    "sol_status_done": {"en": "Response ready", "es": "Respuesta lista"},
    "toast_sol_ready": {"en": "Sol is connected and ready", "es": "Sol está conectada y lista"},
    "quick_q_header": {"en": "Quick questions", "es": "Preguntas rápidas"},
    "sol_sidebar_header": {"en": "### :material/mic: Sol", "es": "### :material/mic: Sol"},
    "sol_key_loaded": {
        "en": "Connection key loaded from app secrets.",
        "es": "Clave de conexión cargada desde los secretos de la app.",
    },
    "sol_key_input_label": {"en": "API key", "es": "API key"},
    "sol_key_help": {
        "en": "Paste it here to activate Sol. It's not saved anywhere.",
        "es": "Pégala aquí para activar a Sol. No se guarda en ningún lado.",
    },
    "sol_model_label": {"en": "Response speed", "es": "Velocidad de respuesta"},
    "sol_model_fast": {"en": "Fast (recommended)", "es": "Rápido (recomendado)"},
    "sol_model_standard": {"en": "Standard", "es": "Estándar"},
    "sol_model_help": {
        "en": "The fast tier is the cheapest option, ideal for this demo.",
        "es": "El nivel rápido es la opción más económica, ideal para este demo.",
    },
    "sol_paste_key_info": {
        "en": "Paste your API key in the sidebar to activate Sol.",
        "es": "Pega tu API key en la barra lateral para activar a Sol.",
    },
    "sol_missing_dep": {
        "en": "Missing dependency: run `pip install google-genai` and restart the app.",
        "es": "Falta una dependencia: corre `pip install google-genai` y reinicia la app.",
    },
    "sol_chat_placeholder": {
        "en": "Ask Sol about the results...",
        "es": "Pregúntale a Sol sobre los resultados...",
    },
    "sol_error": {"en": "Sol couldn't respond: {error}", "es": "Sol no pudo responder: {error}"},
    "footer_note": {
        "en": "Note: this demo uses synthetic data representative of a banking portfolio, "
              "built to showcase how the final product would work — not FinBank's real client data.",
        "es": "Nota: este demo usa datos sintéticos representativos de un portafolio bancario, "
              "creado para mostrar cómo funcionaría el producto final — no son datos reales de clientes de FinBank.",
    },
    "lang_selector_label": {"en": "Language", "es": "Idioma"},
    "sidebar_brand_tagline": {
        "en": "Conversational predictive analytics",
        "es": "Analítica predictiva conversacional",
    },
}

LABEL_WORDS = {
    "delinquency": {"en": "delinquency", "es": "morosidad"},
    "churn": {"en": "churn", "es": "deserción"},
}

# Human-readable metadata for every raw feature column used by either model —
# powers the profile card, the dataframe headers and the SHAP chart labels.
FEATURE_META = {
    "monthly_income_cop": {"icon": "payments", "es": "Ingreso mensual", "en": "Monthly income", "fmt": "money"},
    "credit_exposure_cop": {"icon": "bank", "es": "Exposición crediticia", "en": "Credit exposure", "fmt": "money"},
    "avg_days_late_last_year": {"icon": "clock", "es": "Días de mora prom. (12m)", "en": "Avg. days late (12m)", "fmt": "days"},
    "num_active_products": {"icon": "package", "es": "Productos activos", "en": "Active products", "fmt": "int"},
    "credit_utilization": {"icon": "credit_card", "es": "Utilización de crédito", "en": "Credit utilization", "fmt": "pct"},
    "months_with_bank": {"icon": "calendar", "es": "Antigüedad (meses)", "en": "Tenure (months)", "fmt": "int"},
    "product_usage_score": {"icon": "trending_up", "es": "Uso de productos", "en": "Product usage", "fmt": "score"},
    "competitor_rate_inquiries": {"icon": "search", "es": "Consultas a competencia", "en": "Competitor rate inquiries", "fmt": "int"},
    "complaint_count_last_year": {"icon": "campaign", "es": "Quejas (último año)", "en": "Complaints (last year)", "fmt": "int"},
    "active_products_change_6m": {"icon": "sync_alt", "es": "Cambio en productos (6m)", "en": "Product change (6m)", "fmt": "delta"},
    "client_value_score": {"icon": "diamond", "es": "Valor del cliente", "en": "Client value", "fmt": "score"},
}

QUICK_QUESTIONS = [
    {
        "es": "¿Cuántos clientes están en riesgo de morosidad?",
        "en": "How many clients are flagged for delinquency?",
    },
    {
        "es": "¿Qué variables más influyen en la deserción?",
        "en": "What variables most influence churn?",
    },
    {
        "es": "Dame los 5 clientes con mayor riesgo de deserción",
        "en": "Give me the top 5 highest churn-risk clients",
    },
]


def get_lang():
    return st.session_state.get("lang", "es")


def t(key, **kwargs):
    text = TR[key][get_lang()]
    return text.format(**kwargs) if kwargs else text


def label_word(model_name):
    return LABEL_WORDS[model_name][get_lang()]


def feature_label(feature, lang):
    meta = FEATURE_META.get(feature)
    return meta[lang] if meta else feature.replace("_", " ").title()


def feature_icon_svg(feature, size=15):
    name = FEATURE_META.get(feature, {}).get("icon", "info")
    return icon_svg(name, size=size)


def format_feature_value(feature, value):
    fmt = FEATURE_META.get(feature, {}).get("fmt", "float")
    try:
        v = float(value)
    except (TypeError, ValueError):
        return str(value)
    if fmt == "money":
        return f"${v:,.0f}"
    if fmt == "pct":
        return f"{v * 100:.1f}%"
    if fmt == "int":
        return f"{v:,.0f}"
    if fmt == "days":
        return f"{v:.1f}"
    if fmt == "score":
        return f"{v:.2f}"
    if fmt == "delta":
        return f"{'+' if v > 0 else ''}{v:.0f}"
    return f"{v:.2f}"


@st.cache_data(show_spinner=False)
def image_base64(path):
    if not os.path.exists(path):
        return None
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def render_sidebar_brand():
    logo_b64 = image_base64(LOGO_PATH)
    if logo_b64:
        logo_html = (
            '<div style="text-align:center;padding:14px 4px 4px;">'
            '<div style="display:inline-block;background:#fff;border-radius:14px;'
            'padding:10px 16px;box-shadow:0 6px 18px rgba(0,0,0,0.25);">'
            f'<img src="data:image/png;base64,{logo_b64}" style="width:100%;max-width:150px;display:block;" />'
            "</div></div>"
        )
    else:
        logo_html = (
            '<div style="text-align:center;padding:10px 0;">'
            f'<strong style="color:{BRAND_GREEN};font-size:1.2rem;">FinTech Sol</strong></div>'
        )
    st.markdown(
        f'{logo_html}<div class="ftx-sidebar-tagline">{t("sidebar_brand_tagline")}</div>',
        unsafe_allow_html=True,
    )


with st.sidebar:
    render_sidebar_brand()

    _lang_keys = ["es", "en"]
    _lang_labels = {"es": "Español", "en": "English"}
    _current_lang = st.session_state.get("lang", "es")
    _chosen_lang = st.segmented_control(
        "Idioma / Language",
        _lang_keys,
        format_func=lambda k: _lang_labels[k],
        default=_current_lang,
        key="lang_picker",
        label_visibility="collapsed",
    )
    st.session_state["lang"] = _chosen_lang or _current_lang
    st.divider()


# ---------- prediction helpers ----------

@st.cache_resource
def load_model_bundle(name):
    model = joblib.load(os.path.join(MODEL_DIR, f"{name}_model.pkl"))
    with open(os.path.join(MODEL_DIR, f"{name}_meta.json")) as f:
        meta = json.load(f)
    explainer = shap.TreeExplainer(model)
    return model, meta, explainer


def score_new_clients(df, model, meta):
    X = df[meta["features"]]
    proba = model.predict_proba(X)[:, 1]
    out = df.copy()
    out["risk_score"] = proba
    out["flagged"] = out["risk_score"] >= meta["threshold"]
    return out.sort_values("risk_score", ascending=False)


def compute_batch_shap(model, explainer, meta, scored_df):
    """SHAP values for every row in the scored batch (not just one client) —
    used both for the global feature-importance charts and for Sol's tools."""
    X = scored_df[meta["features"]].astype(float)
    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    return pd.DataFrame(shap_values, columns=meta["features"], index=scored_df.index)


@st.cache_data(show_spinner=":material/calculate: Calculando riesgo y generando explicabilidad SHAP…")
def score_and_explain(df, model_name):
    model, meta, explainer = load_model_bundle(model_name)
    scored = score_new_clients(df, model, meta)
    shap_df = compute_batch_shap(model, explainer, meta, scored)
    return scored, shap_df


def risk_donut(label, flagged, total, pct_flagged):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Not flagged", "Flagged"],
                values=[total - flagged, flagged],
                hole=0.68,
                sort=False,
                textinfo="none",
                marker=dict(colors=[BRAND_GREEN, ALERT_RED]),
                hoverinfo="label+percent+value",
            )
        ]
    )
    fig.add_annotation(
        text=f"{pct_flagged:.0f}%",
        x=0.5, y=0.5, showarrow=False,
        font=dict(size=24, color=ALERT_RED, family="Manrope"),
    )
    fig.update_layout(
        title=dict(text=f"{label.capitalize()} risk", font=dict(size=13, family="Manrope")),
        showlegend=False,
        margin=dict(l=10, r=10, t=34, b=10),
        height=200,
        paper_bgcolor="rgba(0,0,0,0)",
    )
    return fig


def stat_card_html(icon, label, value, delta=None, delta_tone="down"):
    delta_html = ""
    if delta:
        arrow = "▲" if delta_tone == "up" else "▼"
        delta_html = f'<div class="ftx-stat-delta {delta_tone}">{arrow} {delta}</div>'
    return (
        f'<div class="ftx-stat-card">'
        f'<div class="ftx-stat-icon">{icon}</div>'
        f'<div class="ftx-stat-label">{label}</div>'
        f'<div class="ftx-stat-value">{value}</div>'
        f"{delta_html}"
        f"</div>"
    )


def kpi_row(scored_df, meta, label):
    total = len(scored_df)
    flagged = int(scored_df["flagged"].sum())
    pct_flagged = flagged / total * 100 if total else 0
    avg_risk = scored_df["risk_score"].mean() * 100 if total else 0

    amount_col = meta.get("amount_column")
    exposure_txt = None
    if amount_col in scored_df.columns:
        exposure_flagged = scored_df.loc[scored_df["flagged"], amount_col].sum()
        exposure_txt = f"${exposure_flagged:,.0f}"

    with st.container(border=True):
        c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1.1])
        with c1:
            st.markdown(stat_card_html(icon_svg("group", 20), t("clients_evaluated"), f"{total}"), unsafe_allow_html=True)
        with c2:
            st.markdown(
                stat_card_html(
                    icon_svg("flag", 20), t("flagged_high_risk", label=label_word(label)), f"{flagged}",
                    delta=f"{pct_flagged:.1f}%", delta_tone="up" if flagged else "down",
                ),
                unsafe_allow_html=True,
            )
        with c3:
            st.markdown(stat_card_html(icon_svg("bar_chart", 20), t("avg_risk_score"), f"{avg_risk:.1f}%"), unsafe_allow_html=True)
        with c4:
            if exposure_txt:
                metric_label = t("exposure_at_risk") if label == "delinquency" else t("client_value_at_risk")
                icon = icon_svg("payments", 20) if label == "delinquency" else icon_svg("diamond", 20)
                st.markdown(stat_card_html(icon, metric_label, exposure_txt), unsafe_allow_html=True)
        with c5:
            st.plotly_chart(
                risk_donut(label, flagged, total, pct_flagged),
                use_container_width=True, config=PLOTLY_CONFIG,
            )


def risk_badge_html(flagged):
    if flagged:
        return f'<span class="ftx-badge high"><span class="ftx-badge-dot"></span>{t("risk_high_badge")}</span>'
    return f'<span class="ftx-badge low"><span class="ftx-badge-dot"></span>{t("risk_low_badge")}</span>'


def client_profile_card_html(row, features):
    items = "".join(
        f'<div class="ftx-profile-item"><div class="lbl">{feature_icon_svg(f)} {feature_label(f, get_lang())}</div>'
        f'<div class="val">{format_feature_value(f, row[f])}</div></div>'
        for f in features
    )
    return f'<div class="ftx-profile-grid">{items}</div>'


# Sequential single-hue ramp (pale mint -> brand green -> deep pine) for "how
# high is this client's raw value for this feature" — the same role blue->red
# plays in the official shap.summary_plot, just recolored to the brand and
# kept distinct from the red/green used elsewhere in the app for risk
# direction (that's a different, orthogonal quantity: x position, not color).
BEESWARM_COLORSCALE = [[0.0, "#EAFBF4"], [0.5, BRAND_GREEN], [1.0, "#0B4432"]]


def shap_beeswarm_chart(shap_df, scored, features, lang):
    """Global SHAP as a beeswarm — the same chart shap.summary_plot(plot_type
    ='dot') draws, rebuilt in Plotly for brand colors + hover. One marker per
    client per feature: x = impact on the risk score, color = whether that
    client's own value for the feature is low or high. Markers are packed
    into a density-aware swarm (binned stacking, deterministic — no RNG) so
    rows with many similar-impact clients form the characteristic tapered
    'violin' shape instead of a flat scatter."""
    order = shap_df[features].abs().mean().sort_values(ascending=True).index.tolist()
    row_step = 0.085
    max_offset = 0.42
    client_ids = scored["client_id"].to_numpy()

    xs, ys, colors, customdata = [], [], [], []
    for row_idx, feat in enumerate(order):
        x = shap_df[feat].to_numpy(dtype=float)
        raw = scored[feat].to_numpy(dtype=float)
        ranks = pd.Series(raw).rank(method="average", pct=True).to_numpy()

        n = len(x)
        n_bins = int(np.clip(n // 2, 12, 45))
        x_min, x_max = x.min(), x.max()
        span = x_max - x_min
        bin_idx = (
            np.zeros(n, dtype=int) if span <= 0
            else np.clip(((x - x_min) / span * n_bins).astype(int), 0, n_bins - 1)
        )

        offsets = np.zeros(n)
        for b in range(n_bins):
            members = np.where(bin_idx == b)[0]
            if len(members) == 0:
                continue
            members = members[np.argsort(x[members])]
            for slot, idx in enumerate(members):
                step = (slot + 1) // 2
                offsets[idx] = step if slot % 2 == 0 else -step
        offsets = np.clip(offsets * row_step, -max_offset, max_offset)

        label = feature_label(feat, lang)
        xs.extend(x.tolist())
        ys.extend((row_idx + offsets).tolist())
        colors.extend(ranks.tolist())
        customdata.extend(
            [label, cid, format_feature_value(feat, val)]
            for cid, val in zip(client_ids, raw)
        )

    fig = go.Figure(go.Scatter(
        x=xs, y=ys, mode="markers",
        marker=dict(
            size=8,
            color=colors, cmin=0, cmax=1,
            colorscale=BEESWARM_COLORSCALE,
            line=dict(width=1, color="#ffffff"),
            colorbar=dict(
                tickvals=[0, 1], ticktext=[t("beeswarm_low"), t("beeswarm_high")],
                thickness=12, len=0.55, outlinewidth=0,
                title=dict(text=t("beeswarm_colorbar_title"), side="right", font=dict(size=11)),
            ),
        ),
        customdata=customdata,
        hovertemplate=(
            "<b>%{customdata[1]}</b> — %{customdata[0]}<br>"
            + t("beeswarm_hover_value") + ": %{customdata[2]}<br>"
            + t("bubble_hover_impact") + ": %{x:.4f}<extra></extra>"
        ),
    ))
    fig.add_vline(x=0, line_color="rgba(39,39,39,0.25)")
    fig.update_layout(
        yaxis=dict(
            tickmode="array", tickvals=list(range(len(order))),
            ticktext=[feature_label(f, lang) for f in order],
            zeroline=False,
        ),
        xaxis_title=t("shap_value_axis"),
        margin=dict(l=10, r=10, t=10, b=40), height=90 + len(order) * 48,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=BRAND_DARK, family="Manrope"),
        showlegend=False,
    )
    return fig


def shap_explanation_from_cache(shap_df, row_index):
    return shap_df.loc[row_index].sort_values()


def local_shap_chart(contrib_series, lang):
    s = contrib_series.sort_values()
    labels = [feature_label(f, lang) for f in s.index]
    colors = [ALERT_RED if v > 0 else BRAND_GREEN for v in s.values]
    fig = go.Figure(go.Bar(
        x=s.values, y=labels, orientation="h",
        marker=dict(color=colors),
        hovertemplate="%{y}: %{x:.4f}<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=10), height=280,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=BRAND_DARK, family="Manrope"),
    )
    fig.add_vline(x=0, line_color="rgba(39,39,39,0.25)")
    return fig


def risk_histogram(scored, meta):
    threshold_pct = meta["threshold"] * 100
    fig = go.Figure(go.Histogram(
        x=scored["risk_score"] * 100, nbinsx=20,
        marker=dict(color=BRAND_GREEN, line=dict(color="#ffffff", width=1)),
        hovertemplate="%{x:.1f}%<br>%{y}<extra></extra>",
    ))
    fig.add_vline(
        x=threshold_pct, line_dash="dash", line_color=ALERT_RED, line_width=2,
        annotation_text=t("threshold_label", pct=f"{threshold_pct:.0f}%"),
        annotation_position="top",
    )
    fig.update_layout(
        margin=dict(l=10, r=10, t=30, b=40), height=320, bargap=0.05,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=BRAND_DARK, family="Manrope"),
        xaxis_title=t("risk_pct_axis"), yaxis_title=t("client_count_axis"),
    )
    return fig


def risk_ranking_chart(scored):
    df_sorted = scored.sort_values("risk_score", ascending=False)
    colors = [ALERT_RED if f else BRAND_GREEN for f in df_sorted["flagged"]]
    fig = go.Figure(go.Bar(
        x=df_sorted["client_id"], y=df_sorted["risk_score"] * 100,
        marker=dict(color=colors),
        hovertemplate="%{x}: %{y:.1f}%<extra></extra>",
    ))
    fig.update_layout(
        margin=dict(l=10, r=10, t=10, b=70), height=360,
        plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color=BRAND_DARK, family="Manrope"),
        yaxis_title=t("risk_pct_axis"), xaxis=dict(tickangle=-45),
    )
    return fig


def view_selector(model_name):
    keys = ["table", "charts", "explain"]
    labels = {
        "table": f":material/table_rows: {t('view_table')}",
        "charts": f":material/bar_chart: {t('view_charts')}",
        "explain": f":material/insights: {t('view_explain')}",
    }
    selected = st.segmented_control(
        t("view_selector_label"), keys, format_func=lambda k: labels[k],
        default="table", key=f"view_{model_name}", label_visibility="collapsed",
    )
    return selected or "table"


def render_table_view(scored, meta, lang):
    table = scored[["client_id", "flagged"]].copy()
    table["risk_pct"] = scored["risk_score"] * 100
    for f in meta["features"]:
        fmt = FEATURE_META.get(f, {}).get("fmt")
        table[f] = scored[f] * 100 if fmt == "pct" else scored[f]

    column_config = {
        "client_id": st.column_config.TextColumn(t("col_client_id")),
        "flagged": st.column_config.CheckboxColumn(t("col_flagged"), disabled=True),
        "risk_pct": st.column_config.ProgressColumn(
            t("col_risk_score"), format="%.1f%%", min_value=0, max_value=100,
        ),
    }
    for f in meta["features"]:
        label = feature_label(f, lang)
        fmt = FEATURE_META.get(f, {}).get("fmt")
        if fmt in ("money",):
            column_config[f] = st.column_config.NumberColumn(label, format="$%.0f")
        elif fmt == "pct":
            column_config[f] = st.column_config.NumberColumn(label, format="%.1f%%")
        elif fmt == "delta":
            column_config[f] = st.column_config.NumberColumn(label, format="%+.0f")
        elif fmt == "score":
            column_config[f] = st.column_config.NumberColumn(label, format="%.2f")
        elif fmt == "days":
            column_config[f] = st.column_config.NumberColumn(label, format="%.1f")
        else:
            column_config[f] = st.column_config.NumberColumn(label, format="%.0f")

    column_order = ["client_id", "flagged", "risk_pct"] + meta["features"]
    st.dataframe(
        table, column_config=column_config, column_order=column_order,
        hide_index=True, use_container_width=True, height=340,
    )


def render_charts_view(scored, meta):
    with st.container(border=True):
        st.caption(t("hist_caption"))
        st.plotly_chart(risk_histogram(scored, meta), use_container_width=True, config=PLOTLY_CONFIG)
    with st.container(border=True):
        st.caption(t("ranking_caption"))
        st.plotly_chart(risk_ranking_chart(scored), use_container_width=True, config=PLOTLY_CONFIG)


def render_explain_view(scored, shap_df, meta, label, lang, model_name):
    st.markdown(t("global_shap_header"))
    st.caption(t("global_shap_caption", n=len(scored), label=label_word(label)))
    st.caption(t("beeswarm_caption"))
    st.plotly_chart(
        shap_beeswarm_chart(shap_df, scored, meta["features"], lang),
        use_container_width=True, config=PLOTLY_CONFIG,
    )

    st.divider()
    st.markdown(t("local_shap_header"))
    client_options = scored["client_id"].tolist()
    selected_client = st.selectbox(t("select_client"), client_options, key=f"select_{model_name}")
    row = scored[scored["client_id"] == selected_client].iloc[0]
    contrib = shap_explanation_from_cache(shap_df, row.name)

    st.markdown(
        f'<div class="ftx-client-header">'
        f'<span class="ftx-client-name">{selected_client}</span>'
        f"{risk_badge_html(bool(row['flagged']))}"
        f"</div>",
        unsafe_allow_html=True,
    )
    status = t("flagged_status") if row["flagged"] else t("not_flagged_status")
    st.caption(t("client_risk_caption", client=selected_client, score=f"{row['risk_score']:.1%}", status=status))

    st.markdown(t("client_profile_header"))
    st.markdown(client_profile_card_html(row, meta["features"]), unsafe_allow_html=True)

    st.plotly_chart(
        local_shap_chart(contrib, lang),
        use_container_width=True, config=PLOTLY_CONFIG,
    )


def render_tab(label, model_name, title):
    st.subheader(title)
    lang = get_lang()

    if not os.path.exists(os.path.join(MODEL_DIR, f"{model_name}_model.pkl")):
        st.warning(t("model_not_found"))
        return

    model, meta, _explainer = load_model_bundle(model_name)

    with st.expander(t("about_model"), expanded=False):
        metric_name = "F2-score" if model_name == "delinquency" else "F1-score"
        metric_value = meta.get("f2_score", meta.get("f1_score"))
        st.markdown(
            t(
                "about_model_body",
                target=meta["target"],
                horizon=meta.get("horizon", "N/A"),
                metric_name=metric_name,
                metric_value=metric_value,
                best_params=meta.get("best_params"),
            )
        )

    with st.container(border=True):
        col_up, col_actions = st.columns([2, 1])
        with col_up:
            uploaded = st.file_uploader(t("upload_label", label=label_word(label)), type="csv", key=model_name)
        with col_actions:
            if os.path.exists(NEW_CLIENTS_TEMPLATE):
                with open(NEW_CLIENTS_TEMPLATE, "rb") as f:
                    st.download_button(
                        t("download_sample"), f, file_name="new_clients_template.csv",
                        mime="text/csv", key=f"dl_{model_name}", use_container_width=True,
                    )
            bcol1, bcol2 = st.columns(2)
            clear_clicked = bcol1.button(t("clear_data"), key=f"clear_{model_name}", use_container_width=True)
            reset_clicked = bcol2.button(t("reset_sample"), key=f"reset_{model_name}", use_container_width=True)

    df_key = f"df_{model_name}"
    if df_key not in st.session_state:
        st.session_state[df_key] = (
            pd.read_csv(NEW_CLIENTS_TEMPLATE) if os.path.exists(NEW_CLIENTS_TEMPLATE) else None
        )

    # file_uploader keeps returning the same file across reruns until the
    # user picks a new one or clears it — only (re)process it once per
    # actual upload, so it doesn't stomp on the buttons below.
    last_upload_key = f"_last_upload_id_{model_name}"
    if uploaded is not None and st.session_state.get(last_upload_key) != uploaded.file_id:
        st.session_state[last_upload_key] = uploaded.file_id
        new_df = pd.read_csv(uploaded)
        missing = [c for c in meta["features"] if c not in new_df.columns]
        if missing:
            st.error(t("missing_columns", missing=missing))
            return
        st.session_state[df_key] = new_df
        st.toast(t("toast_uploaded", n=len(new_df)), icon=":material/check_circle:")

    if clear_clicked:
        st.session_state[df_key] = None
        st.toast(t("toast_cleared"), icon=":material/delete:")
    if reset_clicked:
        st.session_state[df_key] = (
            pd.read_csv(NEW_CLIENTS_TEMPLATE) if os.path.exists(NEW_CLIENTS_TEMPLATE) else None
        )
        st.toast(t("toast_reset"), icon=":material/restart_alt:")

    df = st.session_state.get(df_key)
    if df is None:
        st.info(t("no_data_loaded"))
        return

    scored, shap_df = score_and_explain(df, model_name)

    st.session_state[f"scored_{model_name}"] = scored  # used by the Sol chat tab's tools
    st.session_state[f"meta_{model_name}"] = meta
    st.session_state[f"shap_{model_name}"] = shap_df  # same, indexed like `scored`

    st.markdown(t("key_indicators"))
    kpi_row(scored, meta, label)

    view = view_selector(model_name)
    if view == "table":
        st.markdown(t("prioritized_list"))
        render_table_view(scored, meta, lang)
    elif view == "charts":
        st.markdown(t("risk_distribution"))
        render_charts_view(scored, meta)
    else:
        render_explain_view(scored, shap_df, meta, label, lang, model_name)


# ---------- Sol chat (Gemini API, with real tools — not just a text summary) ----------
#
# These functions are passed to Gemini as "tools": the model decides on
# its own when a question needs one of them (e.g. "give me 10 clients to
# call"), calls it, and gets back exact numbers instead of guessing.

def get_kpis(model: str) -> dict:
    """Returns the key indicators (KPIs) for the most recent batch of scored
    clients for a given model.

    Args:
        model: Either 'delinquency' or 'churn'.
    """
    scored = st.session_state.get(f"scored_{model}")
    meta = st.session_state.get(f"meta_{model}", {})
    if scored is None or len(scored) == 0:
        return {"error": f"No {model} predictions have been run yet in this session."}
    return {
        "prediction_horizon": meta.get("horizon"),
        "total_clients_evaluated": int(len(scored)),
        "clients_flagged_high_risk": int(scored["flagged"].sum()),
        "pct_flagged": round(float(scored["flagged"].mean()) * 100, 1),
        "average_risk_score_pct": round(float(scored["risk_score"].mean()) * 100, 1),
        "decision_threshold": meta.get("threshold"),
    }


def get_client_list(model: str, n: int = -1, flagged_only: bool = True) -> list:
    """Returns a prioritized list of clients for a given model, sorted from
    highest to lowest risk score — e.g. to know who to call first.

    Use this both for "give me the full list of clients predicted as
    delinquent/churn" (leave n as -1, the default) and for "give me the
    top N" (set n to whatever number was asked for, e.g. 5, 10, 20).

    Args:
        model: Either 'delinquency' or 'churn'.
        n: How many clients to return. Use -1 (the default) to return ALL
            clients that matched flagged_only — use this when the
            stakeholder asks for "all of them" or "the full list", not a
            specific number. Set to a positive number (5, 10, 20...) only
            when the stakeholder explicitly asks for a top N.
        flagged_only: If True (default), only return clients flagged as
            high risk — this is what "who is predicted to be in
            delinquency/churn" means. If False, return clients regardless
            of flag status (rarely needed).
    """
    scored = st.session_state.get(f"scored_{model}")
    if scored is None or len(scored) == 0:
        return [{"error": f"No {model} predictions have been run yet in this session."}]
    subset = scored[scored["flagged"]] if flagged_only else scored
    result = subset if n is None or n < 0 else subset.head(n)
    return [
        {"client_id": r.client_id, "risk_score_pct": round(r.risk_score * 100, 1)}
        for r in result.itertuples()
    ]


def get_shap_summary(model: str, top_n: int = 5) -> list:
    """Returns which variables most influence the model's predictions
    overall — i.e. which factors most explain why clients get classified
    as high risk (class 1) for delinquency or churn. Use this for questions
    like "what variables most influenced the delinquency model" or "what
    drives churn predictions".

    Args:
        model: Either 'delinquency' or 'churn'.
        top_n: How many top variables to return (default 5).
    """
    shap_df = st.session_state.get(f"shap_{model}")
    if shap_df is None or len(shap_df) == 0:
        return [{"error": f"No {model} predictions have been run yet in this session."}]
    importance = shap_df.abs().mean().sort_values(ascending=False)
    direction = shap_df.mean()
    top = importance.head(top_n)
    return [
        {
            "variable": var,
            "overall_importance": round(float(val), 4),
            "typical_direction": "increases risk" if direction[var] > 0 else "decreases risk",
        }
        for var, val in top.items()
    ]


def get_feature_contribution(model: str, feature: str, client_id: str = None) -> dict:
    """Returns how much a specific variable contributed to the risk score
    (class 1: delinquency or churn) — either for one specific client, or
    on average across all uploaded clients if no client_id is given. Use
    this for questions like "how much did credit_utilization contribute to
    this client's score" or "how much does complaint_count_last_year
    typically contribute to churn risk".

    Args:
        model: Either 'delinquency' or 'churn'.
        feature: The exact variable/column name to check.
        client_id: Optional. If given, returns the contribution for that
            specific client. If omitted, returns the average contribution
            across every client in the current uploaded batch.
    """
    shap_df = st.session_state.get(f"shap_{model}")
    scored = st.session_state.get(f"scored_{model}")
    if shap_df is None or len(shap_df) == 0:
        return {"error": f"No {model} predictions have been run yet in this session."}
    if feature not in shap_df.columns:
        return {"error": f"'{feature}' is not a variable used by the {model} model. "
                          f"Available variables: {list(shap_df.columns)}"}

    if client_id:
        match = scored[scored["client_id"] == client_id]
        if match.empty:
            return {"error": f"Client '{client_id}' not found in the current uploaded batch."}
        value = shap_df.loc[match.index[0], feature]
        return {
            "variable": feature, "client_id": client_id,
            "contribution": round(float(value), 4),
            "direction": "increased" if value > 0 else "decreased",
        }

    avg_value = shap_df[feature].mean()
    return {
        "variable": feature, "scope": "average across all uploaded clients",
        "average_contribution": round(float(avg_value), 4),
        "typical_direction": "increases risk" if avg_value > 0 else "decreases risk",
    }


SOL_SYSTEM_PROMPT = """You are Sol, FinTech Solutions' conversational assistant for FinBank.
Stakeholders ask you, in plain language, about the results of the delinquency
(30/60-day horizon) and churn (3-month horizon) predictive models. Use the
available tools to answer with real numbers — never guess or make up a
client ID, a number, or a variable name.

- get_kpis: overall counts and rates for a model.
- get_client_list: who is flagged (use n=-1 for "everyone" / "the full
  list"; a positive n only when a specific top N is requested).
- get_shap_summary: which variables most drive a model's predictions
  overall (use for "what influences delinquency/churn the most").
- get_feature_contribution: how much one specific variable contributes,
  either for one client or on average across the batch.

SHAP contribution values are relative — describe them as "pushing the risk
score up" or "down", not as exact real-world probabilities.

Language: detect whether the stakeholder wrote in English or Spanish, and
always reply in that same language. If a question mixes both, reply in
Spanish. Never mention that you're detecting language — just answer
naturally in it.

Answer briefly and clearly, like a helpful analyst summarizing results in a
business meeting. If a tool returns an error saying there are no
predictions yet, tell the stakeholder (in their language) to upload a
client file in the Delinquency or Churn tab first."""


def _get_gemini_api_key():
    try:
        key = st.secrets.get("GEMINI_API_KEY", "")
    except Exception:
        key = ""
    return key or os.environ.get("GEMINI_API_KEY", "")


def render_call_card():
    sol_mark_b64 = image_base64(SOL_MARK_PATH)
    if sol_mark_b64:
        avatar_inner = f'<img src="data:image/png;base64,{sol_mark_b64}" style="width:66%;height:66%;object-fit:contain;" />'
    else:
        avatar_inner = icon_svg("sun", 24, color=BRAND_DARK)
    st.markdown(
        f"""
        <div class="ftx-call-card">
          <div class="ftx-call-left">
            <div class="ftx-call-avatar">{avatar_inner}</div>
            <div>
              <div class="ftx-call-name">Sol</div>
              <div class="ftx-call-sub">{t('sol_call_status_demo')}</div>
            </div>
          </div>
          <div class="ftx-call-status">
            <div class="ftx-wave"><span></span><span></span><span></span><span></span><span></span></div>
            {t('sol_call_live')}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_sol_chat():
    render_call_card()
    st.caption(t("sol_caption"))

    configured_key = _get_gemini_api_key()
    with st.sidebar:
        st.markdown(t("sol_sidebar_header"))
        if configured_key:
            api_key_input = configured_key
            st.caption(t("sol_key_loaded"))
        else:
            api_key_input = st.text_input(
                t("sol_key_input_label"), value="", type="password",
                help=t("sol_key_help"),
            ).strip()
        model_ids = ["gemini-flash-latest", "gemini-3.6-flash"]
        model_labels = [t("sol_model_fast"), t("sol_model_standard")]
        model_idx = st.selectbox(
            t("sol_model_label"), range(len(model_ids)),
            format_func=lambda i: model_labels[i], index=0,
            help=t("sol_model_help"),
        )
        model_choice = model_ids[model_idx]

    if not api_key_input:
        st.info(t("sol_paste_key_info"))
        return

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        st.error(t("sol_missing_dep"))
        return

    if "sol_chat" not in st.session_state or st.session_state.get("sol_model") != model_choice:
        client = genai.Client(api_key=api_key_input)
        config = types.GenerateContentConfig(
            system_instruction=SOL_SYSTEM_PROMPT,
            tools=[get_kpis, get_client_list, get_shap_summary, get_feature_contribution],
        )
        st.session_state["sol_client"] = client
        st.session_state["sol_chat"] = client.chats.create(model=model_choice, config=config)
        st.session_state["sol_model"] = model_choice
        st.session_state["sol_history"] = []
        st.toast(t("toast_sol_ready"), icon=":material/check_circle:")

    lang = get_lang()
    st.markdown(f":material/chat: **{t('quick_q_header')}**")
    qcols = st.columns(len(QUICK_QUESTIONS))
    for i, q in enumerate(QUICK_QUESTIONS):
        if qcols[i].button(q[lang], key=f"quickq_{i}", use_container_width=True):
            st.session_state["_pending_sol_msg"] = q[lang]

    for msg in st.session_state["sol_history"]:
        avatar = SOL_AVATAR if msg["role"] == "assistant" else ":material/person:"
        with st.chat_message(msg["role"], avatar=avatar):
            st.write(msg["content"])

    pending_msg = st.session_state.pop("_pending_sol_msg", None)
    typed_msg = st.chat_input(t("sol_chat_placeholder"))
    user_msg = typed_msg or pending_msg
    if user_msg:
        st.session_state["sol_history"].append({"role": "user", "content": user_msg})
        with st.chat_message("user", avatar=":material/person:"):
            st.write(user_msg)

        with st.chat_message("assistant", avatar=SOL_AVATAR):
            try:
                with st.status(t("sol_status_thinking"), expanded=False) as status:
                    response = st.session_state["sol_chat"].send_message(user_msg)
                    status.update(label=t("sol_status_done"), state="complete")
                st.write(response.text)
                st.session_state["sol_history"].append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(t("sol_error", error=e))


# ---------- layout ----------

_logo_b64 = image_base64(LOGO_PATH)
_logo_html = f'<img src="data:image/png;base64,{_logo_b64}" alt="FinTech Sol" />' if _logo_b64 else ""

st.markdown(
    f"""
    <div class="ftx-hero">
      <div class="ftx-hero-left">
        {_logo_html}
        <div>
          <h1>{t('app_title')}</h1>
          <p>{t('app_subtitle')}</p>
        </div>
      </div>
      <div class="ftx-status-row">
        <div class="ftx-chip"><span class="ftx-dot"></span>{t('status_models_active')}</div>
        <div class="ftx-chip">{icon_svg('mic', 14)} {t('status_sol_ready')}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

tab1, tab2, tab3 = st.tabs([
    f":material/trending_down: {t('tab_delinquency')}",
    f":material/person_remove: {t('tab_churn')}",
    f":material/mic: {t('tab_sol')}",
])

with tab1:
    render_tab("delinquency", "delinquency", t("delinquency_title"))

with tab2:
    render_tab("churn", "churn", t("churn_title"))

with tab3:
    render_sol_chat()

st.divider()
st.markdown(f'<div class="ftx-footer">{icon_svg("info", 14)} {t("footer_note")}</div>', unsafe_allow_html=True)
