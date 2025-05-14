import os
import pandas as pd
import yfinance as yf


# --- Configuration ---
TICKERS = [
    "ACEIX", "PWTYX", "OGIAX", "PRWCX", "MDCPX",
    "SWOBX", "PGMAX", "OAKBX", "VGSTX", "GOIAX",
    "MXGPX", "MBAAX", "FSATX"
]
START_DATE = "2017-01-01"
END_DATE = "2024-12-31"
DATA_DIR = "data/performance_traditional"
os.makedirs(DATA_DIR, exist_ok=True)

# --- Download and store prices ---
all_data = []

for ticker in TICKERS:
    print(f"📥 Downloading {ticker}...")
    data = yf.download(ticker, start=START_DATE, end=END_DATE, auto_adjust=True, progress=False)
    if not data.empty:
        close_series = data["Adj Close"]
        close_series.name = ticker  # instead of .rename(ticker) to avoid shadowed str()
        all_data.append(close_series)
    else:
        print(f"⚠️ No data for {ticker}")

# --- Combine all data into one DataFrame ---
if not all_data:
    raise RuntimeError("❌ No valid data downloaded.")

prices_df = pd.concat(all_data, axis=1)
prices_df.index.name = "Date"
prices_df.to_csv(os.path.join(DATA_DIR, "traditional_prices.csv"))

# --- Compute monthly returns ---
monthly_returns = prices_df.resample("ME").last().pct_change().dropna()
monthly_returns.to_csv(os.path.join(DATA_DIR, "traditional_monthly_returns.csv"))

print("✅ Download and export complete.")