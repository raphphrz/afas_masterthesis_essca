import os
import sqlite3
import pandas as pd
import yfinance as yf

# --- Configuration ---
DB_PATH = "../data/portfolio_data.db"
TABLE_NAME = "performance_mutual_funds"

# --- List of tickers (example) ---
tickers = ["ACEIX", "PWTYX", "OGIAX", "PRWCX", "MDCPX", "SWOBX", "PGMAX", "OAKBX", "VGSTX", "GOIAX", "MXGPX", "MBAAX", "FSATX"]

# --- Fetch fund metadata using yfinance ---
def get_summary_info(ticker_list):
    records = []
    for ticker in ticker_list:
        try:
            print(f"Fetching: {ticker}")
            info = yf.Ticker(ticker).info
            records.append({
                "Ticker": ticker,
                "Name": info.get("longName"),
                "Currency": info.get("currency"),
                "Asset Class": info.get("quoteType"),
                "Expense Ratio": info.get("annualReportExpenseRatio"),
                "Net Assets": info.get("totalAssets"),
                "Inception Date": info.get("fundInceptionDate"),
                "Morningstar Rating": info.get("morningStarOverallRating")
            })
        except Exception as e:
            print(f"❌ Error for {ticker}: {e}")
            records.append({
                "Ticker": ticker,
                "Name": None,
                "Currency": None,
                "Asset Class": None,
                "Expense Ratio": None,
                "Net Assets": None,
                "Inception Date": None,
                "Morningstar Rating": None
            })
    return pd.DataFrame(records)

# --- Insert or update in SQLite database ---
def insert_into_sqlite(df):
    if not os.path.exists(os.path.dirname(DB_PATH)):
        os.makedirs(os.path.dirname(DB_PATH))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
            Ticker TEXT PRIMARY KEY,
            Name TEXT,
            Currency TEXT,
            Asset_Class TEXT,
            Expense_Ratio REAL,
            Net_Assets REAL,
            Inception_Date TEXT,
            Morningstar_Rating INTEGER
        )
    """)

    for _, row in df.iterrows():
        cursor.execute(f"""
            INSERT INTO {TABLE_NAME} (Ticker, Name, Currency, Asset_Class, Expense_Ratio, Net_Assets, Inception_Date, Morningstar_Rating)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(Ticker) DO UPDATE SET
                Name=excluded.Name,
                Currency=excluded.Currency,
                Asset_Class=excluded.Asset_Class,
                Expense_Ratio=excluded.Expense_Ratio,
                Net_Assets=excluded.Net_Assets,
                Inception_Date=excluded.Inception_Date,
                Morningstar_Rating=excluded.Morningstar_Rating
        """, (
            row.get("Ticker"),
            row.get("Name"),
            row.get("Currency"),
            row.get("Asset Class"),
            row.get("Expense Ratio"),
            row.get("Net Assets"),
            row.get("Inception Date"),
            row.get("Morningstar Rating")
        ))

    conn.commit()
    conn.close()
    print(f"✅ {len(df)} records inserted/updated in '{TABLE_NAME}'")

# --- Run process ---
if __name__ == "__main__":
    summary_df = get_summary_info(tickers)
    insert_into_sqlite(summary_df)