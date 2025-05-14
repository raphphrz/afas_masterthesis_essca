import pandas as pd
import numpy as np
import os

# --- Config ---
RETURNS_FILE = "data/performance_traditional/traditional_monthly_returns.csv"
ANNUAL_RETURNS_FILE = "data/performance_traditional/traditional_annual_returns.csv"
EXPORT_FILE = "data/performance_traditional/traditional_performance_stats.csv"

# US 10Y yields (risk-free rate per year)
rf_table = {
    2018: 0.0291,
    2019: 0.0214,
    2020: 0.0089,
    2021: 0.0145,
    2022: 0.0339,
    2023: 0.0388,
    2024: 0.0410
}
rf_1y = np.mean([rf_table[y] for y in [2024]])
rf_3y = np.mean([rf_table[y] for y in [2022, 2023, 2024]])
rf_7y = np.mean([rf_table[y] for y in [2018, 2019, 2020, 2021, 2022, 2023, 2024]])

# --- Load data ---
monthly_df = pd.read_csv(RETURNS_FILE, index_col="Date", parse_dates=True)
annual_df = pd.read_csv(ANNUAL_RETURNS_FILE)

# --- Define periods ---
monthly_df = monthly_df.sort_index()
PERIODS = {
    "1y": monthly_df.loc["2024"],
    "3y": monthly_df.loc["2022":"2024"],
    "7y": monthly_df.loc["2018":"2024"]
}

# --- Compute all stats ---
results = []

for ticker in monthly_df.columns:
    entry = {"Ticker": ticker}

    for label, period_df in PERIODS.items():
        if ticker in period_df.columns:
            returns = period_df[ticker].dropna()
            if len(returns) >= 10:
                std_monthly = returns.std()
                vol_ann = std_monthly * np.sqrt(12)
                entry[f"{label}_volatility"] = round(vol_ann * 100, 2)

                # Sharpe ratio
                ann_return_row = annual_df[annual_df["Ticker"] == ticker]
                if not ann_return_row.empty:
                    r_ann = ann_return_row[f"{label}_return"].values[0] / 100
                    rf = {"1y": rf_1y, "3y": rf_3y, "7y": rf_7y}[label]
                    sharpe = (r_ann - rf) / vol_ann if vol_ann > 0 else np.nan
                    entry[f"{label}_sharpe"] = round(sharpe, 2)
                else:
                    entry[f"{label}_sharpe"] = np.nan
            else:
                entry[f"{label}_volatility"] = np.nan
                entry[f"{label}_sharpe"] = np.nan

    results.append(entry)

# --- Merge and export ---
stats_df = pd.DataFrame(results)
final_df = pd.merge(annual_df, stats_df, on="Ticker", how="left")
final_df.to_csv(EXPORT_FILE, index=False)

print("✅ Exported full performance data with volatility & Sharpe ratios:", EXPORT_FILE)