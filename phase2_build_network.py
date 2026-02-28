import pandas as pd
import numpy as np

# =============================
# LOAD PHASE 1 DATA
# =============================
df = pd.read_csv("phase1_clean_shock_data.csv")
df["date"] = pd.to_datetime(df["date"])

# -----------------------------
# PARAMETERS
# -----------------------------
WINDOW = 60          # rolling window (days)
CORR_THRESHOLD = 0.3 # edge threshold
MIN_OBS = 50         # minimum overlapping observations

# -----------------------------
# PIVOT RETURNS
# -----------------------------
returns = (
    df.pivot(index="date", columns="stock", values="return")
    .sort_index()
)

# -----------------------------
# BUILD NETWORK SNAPSHOTS
# -----------------------------
networks = {}

dates = returns.index

for t in range(WINDOW, len(dates)):
    window_returns = returns.iloc[t-WINDOW:t]

    corr = window_returns.corr(min_periods=MIN_OBS)

    edges = []
    for i in corr.columns:
        for j in corr.columns:
            if i >= j:
                continue

            w = corr.loc[i, j]
            if pd.notna(w) and abs(w) >= CORR_THRESHOLD:
                edges.append((i, j, w))

    networks[dates[t]] = edges

print(f"✅ Built {len(networks)} rolling correlation networks")

# -----------------------------
# SAVE ONE SNAPSHOT (for sanity check)
# -----------------------------
sample_date = list(networks.keys())[0]
sample_edges = networks[sample_date]

sample_df = pd.DataFrame(
    sample_edges,
    columns=["stock_i", "stock_j", "correlation"]
)

sample_df.to_csv("phase2_sample_network.csv", index=False)

print("📁 Sample network saved: phase2_sample_network.csv")
