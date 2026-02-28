import pandas as pd
import numpy as np

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("./data/stocks_df.csv")

# Standardize column names
df.columns = df.columns.str.lower()

# Rename for clarity
df = df.rename(columns={
    "stock": "stock",
    "date": "date",
    "close": "close"
})

# Parse dates
df["date"] = pd.to_datetime(df["date"])

# Sort properly (panel structure)
df = df.sort_values(["stock", "date"])

# =============================
# COMPUTE RETURNS
# =============================
df["log_price"] = np.log(df["close"])
df["return"] = df.groupby("stock")["log_price"].diff()

# =============================
# ROLLING VOLATILITY (20 days)
# =============================
WINDOW = 20

df["volatility"] = (
    df.groupby("stock")["return"]
      .rolling(WINDOW)
      .std()
      .reset_index(level=0, drop=True)
)

# =============================
# DEFINE REAL VOLATILITY SHOCKS
# =============================
def label_shocks(group):
    high = group["volatility"].quantile(0.95)
    low = group["volatility"].quantile(0.05)

    group["shock"] = 0
    group.loc[group["volatility"] >= high, "shock"] = 1
    group.loc[group["volatility"] <= low, "shock"] = -1
    return group

df = df.groupby("stock", group_keys=False).apply(label_shocks)

# =============================
# SAVE OUTPUT
# =============================
df.to_csv("phase1_clean_shock_data.csv", index=False)

print("✅ Phase 1 complete: real volatility shocks computed using full dataset")
