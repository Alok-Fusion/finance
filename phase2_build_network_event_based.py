import pandas as pd
import numpy as np

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("phase1_clean_shock_data.csv")
df["date"] = pd.to_datetime(df["date"])

# -----------------------------
# PARAMETERS
# -----------------------------
CORR_THRESHOLD = 0.3
MIN_OBS = 50

# -----------------------------
# SPLIT REGIMES
# -----------------------------
normal_df = df[df["shock"] == "normal"]
shock_df  = df[df["shock"] != "normal"]

def build_network(data, name):
    returns = (
        data.pivot(index="date", columns="stock", values="return")
        .dropna(axis=1, thresh=MIN_OBS)
    )

    corr = returns.corr(min_periods=MIN_OBS)

    edges = []
    for i in corr.columns:
        for j in corr.columns:
            if i >= j:
                continue
            w = corr.loc[i, j]
            if pd.notna(w) and abs(w) >= CORR_THRESHOLD:
                edges.append((i, j, w))

    net_df = pd.DataFrame(edges, columns=["stock_i", "stock_j", "weight"])
    net_df.to_csv(f"phase2_{name}_network.csv", index=False)
    print(f"✅ {name.capitalize()} network saved with {len(net_df)} edges")

# -----------------------------
# BUILD NETWORKS
# -----------------------------
build_network(normal_df, "normal")
build_network(shock_df, "shock")

