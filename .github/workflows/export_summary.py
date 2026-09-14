import os
import sys
import pickle
import pandas as pd

pkl_path = "results/Data/last_screened_results.pkl"
summary_file = os.environ.get("GITHUB_STEP_SUMMARY")

if not os.path.exists(pkl_path):
    print("No last_screened_results.pkl found.")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("\n> ℹ️ **No stocks matched this specific filter criteria today.** Try running a broader index like Nifty 500 or option `0 - Full Technical Screening`.\n")
    sys.exit(0)

try:
    with open(pkl_path, "rb") as f:
        df = pickle.load(f)
except Exception as e:
    print(f"Error loading pickle: {e}")
    sys.exit(0)

if not isinstance(df, pd.DataFrame) or len(df) == 0:
    print("Empty results dataframe.")
    if summary_file:
        with open(summary_file, "a", encoding="utf-8") as f:
            f.write("\n> ℹ️ **0 stocks matched this criteria today.**\n")
    sys.exit(0)

os.makedirs("results/Reports", exist_ok=True)
try:
    df.to_excel("results/Reports/PKScreener_Screened_Stocks.xlsx")
    df.to_csv("results/Reports/PKScreener_Screened_Stocks.csv")
except Exception as e:
    print(f"Error saving excel: {e}")

print(f"Successfully processed {len(df)} screened stocks.")

cols = [c for c in ['LTP', '%Chng', 'RSI', 'volume', 'MA-Signal', 'Trend(22Prds)', 'Pattern'] if c in df.columns]
table_df = df[cols].reset_index()

if summary_file:
    with open(summary_file, "a", encoding="utf-8") as f:
        f.write(f"\n### 🎯 Screened Stocks Table ({len(df)} Stocks Found)\n\n")
        try:
            f.write(table_df.to_markdown(index=False) + "\n")
        except Exception:
            f.write("```text\n" + table_df.to_string(index=False) + "\n```\n")
        f.write("\n> 📥 *You can also download the full Excel file (`PKScreener_Screened_Stocks.xlsx`) from the Artifacts section below.*\n")
