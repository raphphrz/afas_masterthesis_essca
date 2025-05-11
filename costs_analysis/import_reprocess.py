import sqlite3
import pandas as pd

# --- Configuration ---
CSV_PATH = "data/portfolios_reprocessed.csv"
DB_PATH = "../data/portfolio_data.db"
TABLE_NAME = "portfolios_reprocessed"

try:
    # Parse the 'document_date' column as a datetime object
    df = pd.read_csv(CSV_PATH, parse_dates=["document_date"], dayfirst=True)
except FileNotFoundError:
    raise FileNotFoundError(f"CSV file '{CSV_PATH}' not found. Please upload it.")

# Normalize column names
expected_columns = [
    "id", "portfolio_id", "advisor_type", "platform_name", "fund_name",
    "expense_ratio", "transaction_costs", "turnover_rate", "tax_efficiency",
    "assets_under_management", "document_date", "extraction_notes", "excluded"
]
df.columns = [col.strip().lower().replace(" ", "_") for col in df.columns]

# Ensure 'document_date' is properly formatted as datetime
if "document_date" in df.columns:
    df["document_date"] = pd.to_datetime(df["document_date"], errors="coerce", dayfirst=True)

# Check column integrity
if not all(col in df.columns for col in expected_columns):
    missing = set(expected_columns) - set(df.columns)
    raise ValueError(f"Missing expected columns in CSV: {missing}")

# --- Connect to SQLite ---
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

cursor.execute(f'''
    CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        id INTEGER PRIMARY KEY,
        portfolio_id TEXT UNIQUE,
        advisor_type TEXT,
        platform_name TEXT,
        fund_name TEXT,
        expense_ratio REAL,
        transaction_costs REAL,
        turnover_rate REAL,
        tax_efficiency REAL,
        assets_under_management REAL,
        document_date DATETIME,
        extraction_notes TEXT,
        excluded TEXT,
        FOREIGN KEY (portfolio_id) REFERENCES portfolios(portfolio_id)
    )
''')

# Insert or update data
print("Importing data into table 'portfolios_reprocess'...")
for _, row in df.iterrows():
    cursor.execute(f'''
        INSERT INTO {TABLE_NAME} (
            portfolio_id, advisor_type, platform_name, fund_name,
            expense_ratio, transaction_costs, turnover_rate,
            tax_efficiency, assets_under_management,
            document_date, extraction_notes, excluded
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(portfolio_id) DO UPDATE SET
            advisor_type=excluded.advisor_type,
            platform_name=excluded.platform_name,
            fund_name=excluded.fund_name,
            expense_ratio=excluded.expense_ratio,
            transaction_costs=excluded.transaction_costs,
            turnover_rate=excluded.turnover_rate,
            tax_efficiency=excluded.tax_efficiency,
            assets_under_management=excluded.assets_under_management,
            document_date=excluded.document_date,
            extraction_notes=excluded.extraction_notes,
            excluded=excluded.excluded
    ''', (
        row["portfolio_id"], row["advisor_type"], (row["platform_name"] if row["platform_name"] != 0 else ""), row["fund_name"],
        row["expense_ratio"], row["transaction_costs"], row["turnover_rate"],
        row["tax_efficiency"], row["assets_under_management"],
        row["document_date"].strftime('%Y-%m-%d %H:%M:%S') if pd.notnull(row["document_date"]) else None,
        row["extraction_notes"], row["excluded"]
    ))

# Commit and close
conn.commit()
conn.close()
print("✅ Import complete.")