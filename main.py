import os
import sqlite3
import fitz  # PyMuPDF
import openai
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import re
from datetime import datetime
from dotenv import load_dotenv

# Load API key
load_dotenv()
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Paths
ADV_FOLDER = "adv_form"
DB_PATH = "portfolio_data.db"
PROCESSED_FOLDER = "processed"

# Database setup
def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS portfolios (
            portfolio_id TEXT PRIMARY KEY,
            advisor_type TEXT NOT NULL,
            platform_name TEXT NOT NULL,
            fund_name TEXT,
            expense_ratio REAL,
            transaction_costs REAL,
            turnover_rate REAL,
            tax_efficiency REAL,
            assets_under_management REAL,
            document_date TEXT,
            extraction_notes TEXT
        )
    ''')
    conn.commit()
    return conn, cursor

# PDF text extraction
class ADVExtractor:
    def __init__(self, filepath):
        self.filepath = filepath

    def extract_text(self):
        with fitz.open(self.filepath) as doc:
            return " ".join(page.get_text() for page in doc)

    def get_fee_structure(self):
        text = self.extract_text()
        prompt = f"""
        From the following SEC Form ADV text, assume an investment of $500,000 with a 50/50 allocation between equities and bonds.

        Extract only if explicitly stated in the text (do not infer or invent):
        - The name of the platform or advisory firm
        - The type of advisory model: Robo-advisor, Hybrid, or Traditional
        - If available, the name of the fund or strategy being managed
        - The highest applicable management fee (numeric %, for a $500,000 investment)
        - The applicable transaction or trading fees (numeric %, if any)
        - A portfolio turnover rate (float %, only if explicitly mentioned)
        - The assets under management (AUM) if disclosed (numeric only)
        - A numeric estimate of tax efficiency on a 0-10 scale, based on the following standardized rule:
          Tax efficiency score is computed based on the presence of up to five features: (1) tax-loss harvesting, (2) tax-optimized asset location,
          (3) use of ETFs or index funds, (4) turnover rate < 50%, (5) client-specific tax optimization; 2 points each, capped at 10.
        - The document date (e.g. "as of February 28, 2025")

        If any of these data points are not present in the document, leave them blank.
        Do not create or guess any value. Do not make assumptions.

        Also include a short paragraph explaining how each figure was sourced.

        Document Text:
        {text}

        Provide the response in this format:
        Platform: <name>
        Advisor Type: <Robo/Hybrid/Traditional>
        Fund Name: <name or blank>
        Management Fees: <numeric value or blank>
        Transaction Fees: <numeric value or blank>
        AUM: <numeric value or blank>
        Turnover Rate: <percentage as float or blank>
        Tax Efficiency: <numeric 0-10 scale or blank>
        Document Date: <YYYY-MM-DD or blank>
        Notes: <short paragraph explaining sources or estimations>
        """
        response = client.chat.completions.create(
            model='gpt-4.1-mini',
            messages=[
                {"role": "system", "content": "You are a financial data extraction assistant. Do not infer or fabricate data."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.0
        )
        return response.choices[0].message.content

# Parse response and insert into DB
def parse_and_insert(response_text, portfolio_id, cursor):
    try:
        platform = re.search(r"Platform: (.+)", response_text).group(1).strip()
        advisor_type = re.search(r"Advisor Type: (.+)", response_text).group(1).strip()
        fund_name_match = re.search(r"Fund Name: (.*)", response_text)
        fund_name = fund_name_match.group(1).strip() if fund_name_match else ""

        def safe_extract(pattern):
            match = re.search(pattern, response_text)
            return float(match.group(1)) if match else None

        mgmt_fee = safe_extract(r"Management Fees: ([\d.]+)")
        txn_fee = safe_extract(r"Transaction Fees: ([\d.]+)")
        turnover = safe_extract(r"Turnover Rate: ([\d.]+)")
        tax_eff = safe_extract(r"Tax Efficiency: ([\d.]+)")

        aum_match = re.search(r"AUM: \$?([\d,\.]+)", response_text)
        aum = float(aum_match.group(1).replace(',', '')) if aum_match else None

        doc_date_match = re.search(r"Document Date: (\d{4}-\d{2}-\d{2})", response_text)
        document_date = doc_date_match.group(1) if doc_date_match else ""

        notes_match = re.search(r"Notes: (.+)", response_text, re.DOTALL)
        notes = notes_match.group(1).strip() if notes_match else ""

        if mgmt_fee is None and txn_fee is None and turnover is None and tax_eff is None and aum is None:
            print(f"Skipping {portfolio_id}: no extractable numeric data.")
            return

        cursor.execute('''
            INSERT OR REPLACE INTO portfolios (
                portfolio_id, advisor_type, platform_name, fund_name,
                expense_ratio, transaction_costs, turnover_rate, 
                tax_efficiency, assets_under_management, 
                document_date, extraction_notes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (
            portfolio_id,
            advisor_type,
            platform,
            fund_name,
            mgmt_fee,
            txn_fee,
            turnover,
            tax_eff,
            aum,
            document_date,
            notes
        ))
    except Exception as e:
        print(f"Failed to insert {portfolio_id}: {e}")

# Extraction and insertion loop
def process_adv_forms():
    conn, cursor = init_db()
    count = 0
    for filename in os.listdir(ADV_FOLDER):
        if filename.endswith(".pdf"):
            portfolio_id = f"RA_{count:03d}"
            path = os.path.join(ADV_FOLDER, filename)
            extractor = ADVExtractor(path)
            print(f"Processing {filename}...")
            response = extractor.get_fee_structure()
            print(response)
            parse_and_insert(response, portfolio_id, cursor)
            conn.commit()
            count += 1

            #move into processed folder
            if not os.path.exists(PROCESSED_FOLDER):
                os.makedirs(PROCESSED_FOLDER)

            processed_path = os.path.join(PROCESSED_FOLDER, filename)
            os.rename(path, processed_path)
            print(f"Inserted {portfolio_id} into database.")

    print(f"Processed {count} files.")
    conn.close()
# Data visualization

# Analysis preparation
def load_data():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("SELECT * FROM portfolios", conn)
    conn.close()
    return df

def show_descriptive_stats(df):
    print("\nDescriptive Statistics:\n", df.describe())

def plot_costs(df):
    sns.set(style="whitegrid")
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='advisor_type', y='expense_ratio', data=df)
    plt.title('Expense Ratios by Advisor Type')
    plt.show()

# Main runner
if __name__ == "__main__":
    process_adv_forms()
    df = load_data()
    show_descriptive_stats(df)
    # plot_costs(df)
