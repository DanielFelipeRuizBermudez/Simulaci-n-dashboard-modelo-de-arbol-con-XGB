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
import pandas as pd
import shap
import streamlit as st

BASE_DIR = os.path.dirname(__file__)
MODEL_DIR = os.path.join(BASE_DIR, "models")
DATA_DIR = os.path.join(BASE_DIR, "data")
ASSETS_DIR = os.path.join(BASE_DIR, "assets")
NEW_CLIENTS_TEMPLATE = os.path.join(DATA_DIR, "new_clients_template.csv")

BRAND_GREEN = "#00FCA9"
BRAND_DARK = "#272727"

st.set_page_config(page_title="FinBank Predictive Analytics", layout="wide", page_icon="📊")

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

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Clients evaluated", f"{total}")
    c2.metric(f"Flagged as high {label} risk", f"{flagged}", f"{pct_flagged:.1f}%")
    c3.metric("Average risk score", f"{avg_risk:.1f}%")
    if exposure_txt:
        metric_label = "Exposure at risk (COP)" if label == "delinquency" else "Client value at risk"
        c4.metric(metric_label, exposure_txt)


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
        st.warning(
            "Model not found. Run `python train_models.py` first "
            "(after `python generate_data.py`)."
        )
        return

    model, meta, explainer = load_model_bundle(model_name)

    with st.expander("ℹ️ About this model", expanded=False):
        metric_name = "F2-score" if model_name == "delinquency" else "F1-score"
        metric_value = meta.get("f2_score", meta.get("f1_score"))
        st.markdown(
            f"""
            Trained by FinTech Solutions on FinBank's historical customer base
            (same base used for both models — this one just uses `{meta['target']}`
            as its response variable, predicting the event within
            **{meta.get('horizon', 'N/A')}**). Validation {metric_name}: **{metric_value}**,
            with hyperparameters and decision threshold both tuned to optimize
            {metric_name}, not accuracy. Best hyperparameters found via grid
            search: `{meta.get('best_params')}`.

            Below, upload a file with **new clients** to score them instantly.
            """
        )

    if os.path.exists(NEW_CLIENTS_TEMPLATE):
        with open(NEW_CLIENTS_TEMPLATE, "rb") as f:
            st.download_button(
                "⬇️ Download sample 'new clients' file (works for both tabs)",
                f, file_name="new_clients_template.csv", mime="text/csv",
                key=f"dl_{model_name}",
            )

    uploaded = st.file_uploader(f"Upload new client data ({label})", type="csv", key=model_name)
    if uploaded is None:
        return

    df = pd.read_csv(uploaded)
    missing = [c for c in meta["features"] if c not in df.columns]
    if missing:
        st.error(f"The uploaded file is missing required columns: {missing}")
        return

    scored = score_new_clients(df, model, meta)
    shap_df = compute_batch_shap(model, explainer, meta, scored)

    st.session_state[f"scored_{model_name}"] = scored  # used by the Sol chat tab's tools
    st.session_state[f"meta_{model_name}"] = meta
    st.session_state[f"shap_{model_name}"] = shap_df  # same, indexed like `scored`

    st.markdown("### 📈 Key indicators")
    kpi_row(scored, meta, label)

    st.markdown("### 🚩 Prioritized client list")
    display_cols = ["client_id", "risk_score", "flagged"] + meta["features"]
    st.dataframe(
        scored[display_cols].style.format({"risk_score": "{:.1%}"}),
        use_container_width=True, height=300,
    )

    st.markdown("### 📊 Risk score distribution")
    st.bar_chart(scored.set_index("client_id")["risk_score"])

    st.markdown("### 🧠 What drives this model overall? (global SHAP)")
    st.caption(
        f"Average influence of each variable across all {len(scored)} uploaded clients "
        f"on being classified as high {label} risk (class 1)."
    )
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Overall importance** (bigger = more influence, either direction)")
        st.bar_chart(shap_df.abs().mean().sort_values(ascending=False))
    with col_b:
        st.markdown("**Direction** (positive = pushes risk up, negative = pushes it down)")
        st.bar_chart(shap_df.mean().sort_values())

    st.markdown("### 🔍 Why was one specific client flagged? (local SHAP)")
    client_options = scored["client_id"].tolist()
    selected_client = st.selectbox("Select a client", client_options, key=f"select_{model_name}")
    row = scored[scored["client_id"] == selected_client].iloc[0]
    contrib = shap_explanation_from_cache(shap_df, row.name)

    st.caption(
        f"Risk score for {selected_client}: **{row['risk_score']:.1%}** "
        f"({'flagged' if row['flagged'] else 'not flagged'}). "
        "Bars to the right push the score up, bars to the left push it down."
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


def render_sol_chat():
    st.subheader("💬 Ask Sol")
    st.caption(
        "Text version of Sol for this demo (the real product uses voice calls). "
        "Works in English or Spanish — Sol replies in whichever language you use. "
        "E.g. \"How many clients are flagged for churn?\" or "
        "\"¿Quiénes están predichos para entrar en mora?\""
    )

    api_key_env = os.environ.get("GEMINI_API_KEY", "")
    with st.sidebar:
        st.markdown("### Sol (Gemini API)")
        api_key_input = st.text_input(
            "Gemini API key", value=api_key_env, type="password",
            help="Get one for free at aistudio.google.com. Paste it here, it's not saved anywhere.",
        )
        model_choice = st.selectbox(
            "Model", ["gemini-2.5-flash", "gemini-2.0-flash"], index=0,
            help="Flash models are the cheapest option, ideal for this demo.",
        )

    if not api_key_input:
        st.info("Paste your Gemini API key in the sidebar to activate Sol.")
        return

    try:
        from google import genai
        from google.genai import types
    except ImportError:
        st.error("Missing dependency: run `pip install google-genai` and restart the app.")
        return

    if "sol_chat" not in st.session_state or st.session_state.get("sol_model") != model_choice:
        client = genai.Client(api_key=api_key_input)
        config = types.GenerateContentConfig(
            system_instruction=SOL_SYSTEM_PROMPT,
            tools=[get_kpis, get_client_list, get_shap_summary, get_feature_contribution],
        )
        st.session_state["sol_chat"] = client.chats.create(model=model_choice, config=config)
        st.session_state["sol_model"] = model_choice
        st.session_state["sol_history"] = []

    for msg in st.session_state["sol_history"]:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_msg = st.chat_input("Ask Sol about the results...")
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
                st.error(f"Sol couldn't respond: {e}")


# ---------- layout ----------

logo_path = os.path.join(ASSETS_DIR, "logo.jpg")
if os.path.exists(logo_path):
    st.image(logo_path, width=260)

st.title("📊 FinBank Predictive Analytics — Live Demo")
st.caption(
    "FinTech Solutions · Explainable XGBoost models for early delinquency and churn detection"
)

tab1, tab2, tab3 = st.tabs(["🔴 Delinquency", "🟢 Churn", "💬 Ask Sol"])

with tab1:
    render_tab("delinquency", "delinquency", "Early Delinquency Detection")

with tab2:
    render_tab("churn", "churn", "Churn Risk Detection")

with tab3:
    render_sol_chat()

st.divider()
st.caption(
    "Note: this demo uses synthetic data representative of a banking portfolio, "
    "built to showcase how the final product would work — not FinBank's real client data."
)
