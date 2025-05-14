import pandas as pd
import numpy as np
import os

# --- Config ---
INPUT_FILE = "data/performance_traditional/traditional_prices.csv"
EXPORT_FILE = "data/performance_traditional/traditional_annual_returns.csv"
END_DATE = "2024-12-31"

# --- Load prices ---
df = pd.read_csv(INPUT_FILE, index_col="Date", parse_dates=True)
df = df[df.index <= END_DATE]

# --- Periods ---
periods = {
    "1y": "2023-12-31",
    "3y": "2021-12-31",
    "7y": "2017-12-31",
}

# --- Calculate annualized returns ---
results = []

for ticker in df.columns:
    ticker_data = df[ticker].dropna()
    end_price = ticker_data.loc[:END_DATE].iloc[-1]

    entry = {"Ticker": ticker}

    for label, start in periods.items():
        try:
            start_price = ticker_data.loc[:start].iloc[-1]
            n_years = int(label[0])
            annual_return = (end_price / start_price) ** (1 / n_years) - 1
            entry[f"{label}_return"] = round(annual_return * 100, 2)
        except Exception:
            entry[f"{label}_return"] = np.nan

    results.append(entry)

# --- Save to CSV ---
returns_df = pd.DataFrame(results)
returns_df.to_csv(EXPORT_FILE, index=False)

print("✅ Annualized returns saved to:", EXPORT_FILE)