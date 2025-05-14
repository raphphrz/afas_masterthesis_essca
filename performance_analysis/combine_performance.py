import pandas as pd
import sqlite3
import os

# --- Paths ---
DB_PATH = "../data/portfolio_data.db"
TRAD_FILE = "data/performance_traditional/traditional_performance_stats.csv"
AUTO_FILE = "data/performance_automated/automated_performance_stats.csv"
OUTPUT_FILE = "data/performance_combined/combined_performance_stats.csv"
os.makedirs("data/performance_combined", exist_ok=True)

# --- Load traditional data + fund names ---
trad_df = pd.read_csv(TRAD_FILE)

conn = sqlite3.connect(DB_PATH)
names_df = pd.read_sql_query("SELECT ticker, Name FROM performance_mutual_funds", conn)
conn.close()
names_df.rename(columns={"ticker": "Ticker", "Name": "Fund Name"}, inplace=True)
trad_df = trad_df.merge(names_df, on="Ticker", how="left")
trad_df["Advisor Group"] = "Traditional"

# --- Load automated data ---
auto_df = pd.read_csv(AUTO_FILE)

return_vol_keywords = ["1y_return", "3y_return", "7y_return", "1y_volatility", "3y_volatility", "7y_volatility"]
multiply_cols = [col for col in auto_df.columns if col in return_vol_keywords]

# Apply scaling and round
auto_df[multiply_cols] = auto_df[multiply_cols].apply(lambda x: (x * 100).round(2))

# Complete other fields
auto_df["Fund Name"] = auto_df["Ticker"]
auto_df["Advisor Group"] = "Automated"

# --- Combine datasets ---
combined_df = pd.concat([trad_df, auto_df], ignore_index=True)

# --- Reorder columns ---
cols = ["Advisor Group", "Fund Name", "Ticker"] + [col for col in combined_df.columns if col not in ["Advisor Group", "Fund Name", "Ticker"]]
combined_df = combined_df[cols]

# --- Export ---
combined_df.to_csv(OUTPUT_FILE, index=False)
print(f"✅ Combined file with formatted Sharpe and returns exported to: {OUTPUT_FILE}")