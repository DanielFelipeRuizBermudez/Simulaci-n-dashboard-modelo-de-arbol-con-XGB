"""
Generates ONE synthetic customer base with all the features needed for both
models (delinquency and churn), plus both target/response columns:
  - defaulted_30_60_days  -> target for the delinquency model
  - churned_3_months      -> target for the churn model

This mirrors how it would work with a real FinBank extract: one customer
table, and each model just picks its own response variable and feature
subset from it — you don't need two separate customer populations.

Also writes a single "new clients" template (same columns, no targets) to
upload live during the demo — usable in either the Delinquency or Churn tab.

Class balance is kept realistic (not 50/50): ~15-20% default rate and
~12-16% churn rate, in line with the range reported in credit-scoring
literature (roughly 7%-22% depending on the dataset).
"""

import os

import numpy as np
import pandas as pd

np.random.seed(42)
OUT_DIR = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT_DIR, exist_ok=True)


def generate_customers(n, id_prefix="CL", id_start=100000):
    # --- shared / delinquency-related features ---
    monthly_income_cop = np.random.lognormal(mean=14.7, sigma=0.5, size=n)
    credit_exposure_cop = np.random.lognormal(mean=15.2, sigma=0.7, size=n)
    avg_days_late_last_year = np.random.exponential(scale=8, size=n).clip(0, 120)
    num_active_products = np.random.randint(1, 6, size=n)
    credit_utilization = np.clip(np.random.beta(2, 4, size=n), 0, 1)
    months_with_bank = np.random.randint(1, 180, size=n)

    # --- churn-related features ---
    product_usage_score = np.clip(np.random.beta(3, 2, size=n), 0, 1)
    competitor_rate_inquiries = np.random.poisson(0.4, size=n)
    complaint_count_last_year = np.random.poisson(0.3, size=n)
    active_products_change_6m = np.random.randint(-2, 2, size=n)
    client_value_score = np.clip(np.random.beta(2, 3, size=n), 0, 1)

    # --- target 1: delinquency (30/60-day default) ---
    delinquency_risk = (
        0.035 * avg_days_late_last_year
        + 3.0 * credit_utilization
        - 0.000002 * monthly_income_cop
        + 0.01 * (5 - num_active_products)
        - 0.004 * np.minimum(months_with_bank, 60)
        + np.random.normal(0, 1.1, size=n)
    )
    prob_default = 1 / (1 + np.exp(-(delinquency_risk - delinquency_risk.mean()) / delinquency_risk.std()))
    defaulted_30_60_days = (np.random.rand(n) < np.clip(prob_default * 0.35, 0, 0.95)).astype(int)

    # --- target 2: churn (3-month horizon) ---
    churn_risk = (
        -2.5 * product_usage_score
        + 1.2 * competitor_rate_inquiries
        + 0.8 * complaint_count_last_year
        - 0.7 * active_products_change_6m
        - 0.003 * np.minimum(months_with_bank, 60)
        + np.random.normal(0, 1.0, size=n)
    )
    prob_churn = 1 / (1 + np.exp(-(churn_risk - churn_risk.mean()) / churn_risk.std()))
    churned_3_months = (np.random.rand(n) < np.clip(prob_churn * 0.30, 0, 0.9)).astype(int)

    df = pd.DataFrame({
        "client_id": [f"{id_prefix}{id_start+i}" for i in range(n)],
        "monthly_income_cop": monthly_income_cop.round(0),
        "credit_exposure_cop": credit_exposure_cop.round(0),
        "avg_days_late_last_year": avg_days_late_last_year.round(1),
        "num_active_products": num_active_products,
        "credit_utilization": credit_utilization.round(3),
        "months_with_bank": months_with_bank,
        "product_usage_score": product_usage_score.round(3),
        "competitor_rate_inquiries": competitor_rate_inquiries,
        "complaint_count_last_year": complaint_count_last_year,
        "active_products_change_6m": active_products_change_6m,
        "client_value_score": client_value_score.round(3),
        "defaulted_30_60_days": defaulted_30_60_days,
        "churned_3_months": churned_3_months,
    })
    return df


if __name__ == "__main__":
    historical = generate_customers(6000, id_prefix="CL", id_start=100000)
    historical.to_csv(os.path.join(OUT_DIR, "historical_data.csv"), index=False)

    new_clients = generate_customers(40, id_prefix="NEW", id_start=1000)
    new_clients = new_clients.drop(columns=["defaulted_30_60_days", "churned_3_months"])
    new_clients.to_csv(os.path.join(OUT_DIR, "new_clients_template.csv"), index=False)

    print("Default rate:", historical["defaulted_30_60_days"].mean().round(3))
    print("Churn rate:", historical["churned_3_months"].mean().round(3))
    print("Files written to:", OUT_DIR)
