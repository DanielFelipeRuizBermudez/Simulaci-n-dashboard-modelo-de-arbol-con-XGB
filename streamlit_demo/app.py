"""
FinBank Predictive Analytics Demo — FinTech Solutions
Run with: streamlit run app.py

Requires models already trained: run `python generate_data.py` then
`python train_models.py` first.

For the "Ask Sol" chat tab you need a Gemini API key (from Google AI Studio).
Set it as an environment variable GEMINI_API_KEY, or paste it in the sidebar
when the app is running.
"""

import json
import os

import joblib
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go
import shap
import streamlit as st

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
NEW_CLIENTS_TEMPLATE = os.path.join(DATA_DIR, "new_clients_template.csv")

BRAND_GREEN = "#00FCA9"
BRAND_DARK = "#272727"
ALERT_RED = "#E4572E"

st.set_page_config(page_title="FinBank Predictive Analytics", layout="wide")

st.markdown(
    f"""
    <style>
    .stTabs [data-baseweb="tab-list"] {{ gap: 8px; }}
    .stTabs [aria-selected="true"] {{ color: {BRAND_DARK}; border-bottom-color: {BRAND_GREEN} !important; }}
    div[data-testid="stMetricValue"] {{ color: {BRAND_DARK}; }}
    .stDownloadButton button, .stButton button {{ border-color: {BRAND_GREEN}; }}
    </style>
    """,
    unsafe_allow_html=True,
)


# ---------- i18n ----------
#
# The UI (labels, buttons, headers) is translated via TR below and the t()
# helper. Sol's chat is a separate matter: it already detects the language
# of each question and replies in kind (see SOL_SYSTEM_PROMPT), regardless
# of the UI language chosen here.

TR = {
    "app_title": {
        "en": "FinBank Predictive Analytics — Live Demo",
        "es": "FinBank Analítica Predictiva — Demo en Vivo",
    },
    "app_subtitle": {
        "en": "FinTech Solutions · Explainable XGBoost models for early delinquency and churn detection",
        "es": "FinTech Solutions · Modelos XGBoost explicables para detección temprana de morosidad y deserción de clientes",
    },
    "tab_delinquency": {"en": "Delinquency", "es": "Morosidad"},
    "tab_churn": {"en": "Churn", "es": "Deserción"},
    "tab_sol": {"en": "Ask Sol", "es": "Pregúntale a Sol"},
    "delinquency_title": {"en": "Early Delinquency Detection", "es": "Detección Temprana de Morosidad"},
    "churn_title": {"en": "Churn Risk Detection", "es": "Detección de Riesgo de Deserción"},
    "model_not_found": {
        "en": "Model not found. Run `python train_models.py` first (after `python generate_data.py`).",
        "es": "Modelo no encontrado. Corre `python train_models.py` primero (después de `python generate_data.py`).",
    },
    "about_model": {"en": "About this model", "es": "Sobre este modelo"},
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
        "en": "Download sample 'new clients' file (works for both tabs)",
        "es": "Descargar archivo de ejemplo de 'nuevos clientes' (sirve para ambas pestañas)",
    },
    "upload_label": {"en": "Upload new client data ({label})", "es": "Subir datos de nuevos clientes ({label})"},
    "missing_columns": {
        "en": "The uploaded file is missing required columns: {missing}",
        "es": "Al archivo subido le faltan columnas requeridas: {missing}",
    },
    "clear_data": {"en": "Remove data", "es": "Quitar datos"},
    "reset_sample": {"en": "Restore sample", "es": "Restaurar ejemplo"},
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
    "overall_importance": {
        "en": "**Overall importance** (bigger = more influence, either direction)",
        "es": "**Importancia general** (más grande = más influencia, en cualquier dirección)",
    },
    "direction_header": {
        "en": "**Direction** (positive = pushes risk up, negative = pushes it down)",
        "es": "**Dirección** (positivo = sube el riesgo, negativo = lo baja)",
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
    "flagged_status": {"en": "flagged", "es": "marcado"},
    "not_flagged_status": {"en": "not flagged", "es": "no marcado"},
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
    "sol_sidebar_header": {"en": "### Sol (Gemini API)", "es": "### Sol (API de Gemini)"},
    "sol_key_loaded": {
        "en": "Gemini API key loaded from app secrets.",
        "es": "API key de Gemini cargada desde los secretos de la app.",
    },
    "sol_key_input_label": {"en": "Gemini API key", "es": "API key de Gemini"},
    "sol_key_help": {
        "en": "Get one for free at aistudio.google.com. Paste it here, it's not saved anywhere.",
        "es": "Consigue una gratis en aistudio.google.com. Pégala aquí, no se guarda en ningún lado.",
    },
    "sol_model_help": {
        "en": "Flash models are the cheapest option, ideal for this demo.",
        "es": "Los modelos Flash son la opción más económica, ideal para este demo.",
    },
    "sol_paste_key_info": {
        "en": "Paste your Gemini API key in the sidebar to activate Sol.",
        "es": "Pega tu API key de Gemini en la barra lateral para activar a Sol.",
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
}

LABEL_WORDS = {
    "delinquency": {"en": "delinquency", "es": "morosidad"},
    "churn": {"en": "churn", "es": "deserción"},
}


def get_lang():
    return st.session_state.get("lang", "es")


def t(key, **kwargs):
    text = TR[key][get_lang()]
    return text.format(**kwargs) if kwargs else text


def label_word(model_name):
    return LABEL_WORDS[model_name][get_lang()]


with st.sidebar:
    lang_choice = st.selectbox(
        "Idioma / Language", ["Español", "English"],
        index=0 if get_lang() == "es" else 1,
    )
    st.session_state["lang"] = "es" if lang_choice == "Español" else "en"
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


def risk_donut(label, flagged, total, pct_flagged):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=["Not flagged", "Flagged"],
                values=[total - flagged, flagged],
                hole=0.6,
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
        font=dict(size=28, color=ALERT_RED),
    )
    fig.update_layout(
        title=dict(text=f"{label.capitalize()} risk", font=dict(size=14)),
        showlegend=False,
        margin=dict(l=10, r=10, t=40, b=10),
        width=220, height=220,
    )
    return fig


def kpi_row(scored_df, meta, label):
    total = len(scored_df)
    flagged = int(scored_df["flagged"].sum())
    pct_flagged = flagged / total * 100 if total else 0
    avg_risk = scored_df["risk_score"].mean() * 100 if total else 0

    amount_col = meta.get("amount_column")
    exposure_txt = None
    if amount_col in scored_df.columns:
        exposure_flagged = scored_df.loc[scored_df["flagged"], amount_col].sum()
        exposure_txt = f"{exposure_flagged:,.0f}"

    c1, c2, c3, c4, c5 = st.columns([1, 1, 1, 1, 1.2])
    c1.metric(t("clients_evaluated"), f"{total}")
    c2.metric(t("flagged_high_risk", label=label_word(label)), f"{flagged}", f"{pct_flagged:.1f}%")
    c3.metric(t("avg_risk_score"), f"{avg_risk:.1f}%")
    if exposure_txt:
        metric_label = t("exposure_at_risk") if label == "delinquency" else t("client_value_at_risk")
        c4.metric(metric_label, exposure_txt)

    with c5:
        st.plotly_chart(risk_donut(label, flagged, total, pct_flagged), use_container_width=False)


def compute_batch_shap(model, explainer, meta, scored_df):
    """SHAP values for every row in the scored batch (not just one client) —
    used both for the global feature-importance chart and for Sol's tools."""
    X = scored_df[meta["features"]].astype(float)
    shap_values = explainer.shap_values(X)
    if isinstance(shap_values, list):
        shap_values = shap_values[1]
    return pd.DataFrame(shap_values, columns=meta["features"], index=scored_df.index)


def shap_explanation_from_cache(shap_df, row_index):
    return shap_df.loc[row_index].sort_values()


def render_tab(label, model_name, title):
    st.subheader(title)

    if not os.path.exists(os.path.join(MODEL_DIR, f"{model_name}_model.pkl")):
        st.warning(t("model_not_found"))
        return

    model, meta, explainer = load_model_bundle(model_name)

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

    if os.path.exists(NEW_CLIENTS_TEMPLATE):
        with open(NEW_CLIENTS_TEMPLATE, "rb") as f:
            st.download_button(
                t("download_sample"),
                f, file_name="new_clients_template.csv", mime="text/csv",
                key=f"dl_{model_name}",
            )

    df_key = f"df_{model_name}"
    if df_key not in st.session_state:
        st.session_state[df_key] = (
            pd.read_csv(NEW_CLIENTS_TEMPLATE) if os.path.exists(NEW_CLIENTS_TEMPLATE) else None
        )

    uploaded = st.file_uploader(t("upload_label", label=label_word(label)), type="csv", key=model_name)

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

    col_clear, col_reset = st.columns(2)
    with col_clear:
        if st.button(t("clear_data"), key=f"clear_{model_name}"):
            st.session_state[df_key] = None
    with col_reset:
        if st.button(t("reset_sample"), key=f"reset_{model_name}"):
            st.session_state[df_key] = (
                pd.read_csv(NEW_CLIENTS_TEMPLATE) if os.path.exists(NEW_CLIENTS_TEMPLATE) else None
            )

    df = st.session_state.get(df_key)
    if df is None:
        st.info(t("no_data_loaded"))
        return

    scored = score_new_clients(df, model, meta)
    shap_df = compute_batch_shap(model, explainer, meta, scored)

    st.session_state[f"scored_{model_name}"] = scored  # used by the Sol chat tab's tools
    st.session_state[f"meta_{model_name}"] = meta
    st.session_state[f"shap_{model_name}"] = shap_df  # same, indexed like `scored`

    st.markdown(t("key_indicators"))
    kpi_row(scored, meta, label)

    st.markdown(t("prioritized_list"))
    display_cols = ["client_id", "risk_score", "flagged"] + meta["features"]
    st.dataframe(
        scored[display_cols].style.format({"risk_score": "{:.1%}"}),
        use_container_width=True, height=300,
    )

    st.markdown(t("risk_distribution"))
    st.bar_chart(scored.set_index("client_id")["risk_score"])

    st.markdown(t("global_shap_header"))
    st.caption(t("global_shap_caption", n=len(scored), label=label_word(label)))
    fig = plt.figure()
    shap.summary_plot(
        shap_df.values,
        scored[meta["features"]],
        plot_type="dot",
        max_display=10,
        show=False,
    )
    plt.title(f"SHAP - {label.capitalize()}: Class 1")
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.markdown(t("local_shap_header"))
    client_options = scored["client_id"].tolist()
    selected_client = st.selectbox(t("select_client"), client_options, key=f"select_{model_name}")
    row = scored[scored["client_id"] == selected_client].iloc[0]
    contrib = shap_explanation_from_cache(shap_df, row.name)

    status = t("flagged_status") if row["flagged"] else t("not_flagged_status")
    st.caption(
        t("client_risk_caption", client=selected_client, score=f"{row['risk_score']:.1%}", status=status)
    )
    st.bar_chart(contrib)


# ---------- Sol chat (Gemini API, with real tools — not just a text summary) ----------
#
# These two functions are passed to Gemini as "tools": the model decides on
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


def render_sol_chat():
    st.subheader(t("sol_subheader"))
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
            )
        model_choice = st.selectbox(
            "Model", ["gemini-flash-latest", "gemini-3.6-flash"], index=0,
            help=t("sol_model_help"),
        )

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

    for msg in st.session_state["sol_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_msg = st.chat_input(t("sol_chat_placeholder"))
    if user_msg:
        st.session_state["sol_history"].append({"role": "user", "content": user_msg})
        with st.chat_message("user"):
            st.write(user_msg)

        with st.chat_message("assistant"):
            try:
                response = st.session_state["sol_chat"].send_message(user_msg)
                st.write(response.text)
                st.session_state["sol_history"].append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(t("sol_error", error=e))


# ---------- layout ----------

logo_path = os.path.join(ASSETS_DIR, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=550)

st.title(t("app_title"))
st.caption(t("app_subtitle"))

tab1, tab2, tab3 = st.tabs([t("tab_delinquency"), t("tab_churn"), t("tab_sol")])

with tab1:
    render_tab("delinquency", "delinquency", t("delinquency_title"))

with tab2:
    render_tab("churn", "churn", t("churn_title"))

with tab3:
    render_sol_chat()

st.divider()
st.caption(t("footer_note"))
