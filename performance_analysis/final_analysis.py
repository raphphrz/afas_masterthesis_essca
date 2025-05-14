import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime
from scipy.stats import ttest_ind
import matplotlib.font_manager as fm

# --- Paths & Config ---
INPUT_FILE = "data/performance_combined/combined_performance_stats.csv"
PLOT_DIR = "results/phase2_graphs"
EXPORT_FILE = f"results/phase2_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
os.makedirs(PLOT_DIR, exist_ok=True)

# --- Load data ---
df = pd.read_csv(INPUT_FILE)

# --- Force Times New Roman font ---
plt.rcParams.update({"font.family": "Times New Roman"})  # Set font to Times New Roman

# --- Style configuration ---
sns.set(style="whitegrid")
plt.rcParams.update({
    "axes.edgecolor": "black",
    "axes.linewidth": 1.2,
    "xtick.color": "black",
    "ytick.color": "black",
    "font.family": "Times New Roman"
})

# --- Metrics and labels ---
metrics = {
    "1y_return": "1-Year Return (%)",
    "3y_return": "3-Year Return (%)",
    "7y_return": "7-Year Return (%)",
    "1y_volatility": "1-Year Volatility (%)",
    "3y_volatility": "3-Year Volatility (%)",
    "7y_volatility": "7-Year Volatility (%)",
    "1y_sharpe": "1-Year Sharpe Ratio",
    "3y_sharpe": "3-Year Sharpe Ratio",
    "7y_sharpe": "7-Year Sharpe Ratio"
}

# --- Welch's t-test ---
ttest_results = []
for var, label in metrics.items():
    auto = df[df["Advisor Group"] == "Automated"][var].dropna()
    trad = df[df["Advisor Group"] == "Traditional"][var].dropna()
    t_stat, p_val = ttest_ind(auto, trad, equal_var=False)
    ttest_results.append({
        "Metric": label,
        "Automated Mean": round(auto.mean(), 2),
        "Traditional Mean": round(trad.mean(), 2),
        "t-statistic": round(t_stat, 3),
        "p-value": round(p_val, 4)
    })

# --- Barplots by fund ---
for var, label in metrics.items():
    plt.figure(figsize=(11, 6))
    sns.barplot(
        data=df.sort_values(by=var),
        x="Fund Name", y=var, hue="Advisor Group", dodge=False,
        palette={"Automated": "black", "Traditional": "white"},
        edgecolor="black", linewidth=1.2
    )
    plt.xticks(rotation=90, fontsize=8)
    plt.ylabel(label, fontsize=12)
    plt.xlabel("")
    plt.title(f"{label} by Fund", fontsize=14)
    plt.legend(title="Advisor Group", loc="upper right")
    plt.tight_layout()
    filename = os.path.join(PLOT_DIR, f"{var}_barplot.png")
    plt.savefig(filename, dpi=300)
    plt.close()

# --- Boxplots by group ---
for var, label in metrics.items():
    plt.figure(figsize=(7, 5))
    sns.boxplot(
        data=df, x="Advisor Group", y=var, hue="Advisor Group",
        palette={"Automated": "black", "Traditional": "white"},
        linewidth=1.2, fliersize=3, width=0.6,
        boxprops=dict(edgecolor="black"), medianprops=dict(color="black"),
    )
    plt.ylabel(label, fontsize=12)
    plt.xlabel("")
    plt.title(f"{label} by Advisor Group", fontsize=13)
    plt.tight_layout()
    filename = os.path.join(PLOT_DIR, f"{var}_boxplot.png")
    plt.savefig(filename, dpi=300)
    plt.close()

# --- Export Excel ---
summary_df = pd.DataFrame(ttest_results)
with pd.ExcelWriter(EXPORT_FILE, engine="xlsxwriter") as writer:
    df.to_excel(writer, index=False, sheet_name="Raw Data")
    summary_df.to_excel(writer, index=False, sheet_name="Welch T-Test")

print(f"\n📊 Export completed: {EXPORT_FILE}")
print(f"🖼️ Graphs saved in: {PLOT_DIR}")