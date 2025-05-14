import os
import sqlite3
from datetime import datetime

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend for compatibility

# --- Config ---
DB_PATH = "../data/portfolio_data.db"
TABLE = "portfolios_reprocessed"
PLOT_DIR = "results/plots"
EXPORT_FILE = f"results/cost_analysis_result_{datetime.now().timestamp()}.xlsx"
os.makedirs(PLOT_DIR, exist_ok=True)

# --- Load filtered data (exclude manually flagged rows) ---
conn = sqlite3.connect(DB_PATH)
df = pd.read_sql_query(f"SELECT * FROM {TABLE} WHERE excluded IS NULL OR excluded = 0", conn)
conn.close()

# --- Preprocessing ---
# Create new group: automated (Robo + Hybrid) vs Traditional
AUTOMATED = ["Robo-advisor", "Hybrid"]
df["advisor_group"] = df["advisor_type"].apply(lambda x: "Automated" if x in AUTOMATED else "Traditional")

# Convert AUM to log scale for analysis
df["Log AUM"] = np.log1p(df["assets_under_management"])
df.rename(columns={"expense_ratio": "Expense Ratio", "transaction_costs": "Transaction Costs", "tax_efficiency": "Tax Efficiency"}, inplace=True)

# --- Descriptive Statistics ---
summary = df.groupby("advisor_group")[
    ["Expense Ratio", "Transaction Costs", "Tax Efficiency", "Log AUM"]
].agg(["mean", "std", "median", "count"])

print("\nDescriptive Statistics by Advisor Group:\n")
print(summary)

# --- Visualizations ---
sns.set(style="whitegrid")
plt.rcParams.update({"font.family": "Times New Roman"})  # Set font to Times New Roman
colors = ["#444444", "#888888"]  # Greyscale colors for academic look

for var in ["Expense Ratio", "Transaction Costs", "Tax Efficiency", "Log AUM"]:
    plt.figure(figsize=(8, 5))
    sns.boxplot(x="advisor_group", y=var, data=df, palette=colors)
    plt.title(f"{var} by Advisor Group", fontsize=14)
    plt.ylabel(var, fontsize=12)
    plt.xlabel("")
    plt.xticks(fontsize=11)
    plt.yticks(fontsize=11)
    plt.tight_layout()
    filename = os.path.join(PLOT_DIR, f"{var.replace(' ', '_').lower()}_by_advisor_group.png")
    plt.savefig(filename, dpi=300)
    print(f"Plot saved: {filename}")
    plt.close()

# --- Statistical Tests: Mann–Whitney U ---
def run_mannwhitney(var):
    group1 = df[df["advisor_group"] == "Automated"][var].dropna()
    group2 = df[df["advisor_group"] == "Traditional"][var].dropna()
    return stats.mannwhitneyu(group1, group2, alternative='two-sided')

results = {}
for var in ["Expense Ratio", "Transaction Costs", "Tax Efficiency", "Log AUM"]:
    stat, pval = run_mannwhitney(var)
    results[var] = {"U-statistic": stat, "p-value": pval}

results_df = pd.DataFrame(results).T
results_df.index.name = "Variable"

print("\nMann–Whitney U Test Results:\n")
print(results_df.round(4))

# --- Interpretation ---
print("\nInterpretation Summary:")
for var in results_df.index:
    pval = results_df.loc[var, "p-value"]
    if pval < 0.05:
        print(f"→ Statistically significant difference in {var} (p = {pval:.3f})")
    else:
        print(f"→ No significant difference in {var} (p = {pval:.3f})")

# --- Export to Excel ---
with pd.ExcelWriter(EXPORT_FILE, engine="xlsxwriter") as writer:
    df.to_excel(writer, sheet_name="Raw Data", index=False)
    summary.to_excel(writer, sheet_name="Summary Stats")
    results_df.to_excel(writer, sheet_name="MannWhitneyU")

print(f"\n✅ Analysis exported to {EXPORT_FILE}")
