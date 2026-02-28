import pandas as pd
import numpy as np

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("phase1_clean_shock_data.csv")
shock_net = pd.read_csv("phase2_shock_network.csv")

# -----------------------------
# COMPUTE NETWORK EXPOSURE
# -----------------------------
exposure = {}

for _, row in shock_net.iterrows():
    i, j, w = row["stock_i"], row["stock_j"], row["correlation"]
    exposure[i] = exposure.get(i, 0) + w
    exposure[j] = exposure.get(j, 0) + w

exposure_df = pd.DataFrame(
    exposure.items(),
    columns=["stock", "exposure"]
)

# -----------------------------
# MERGE EXPOSURE INTO MAIN DF
# -----------------------------
df = df.merge(exposure_df, on="stock", how="left").fillna(0)

# -----------------------------
# COMPUTE SHOCK-WEIGHTED IMPACT
# -----------------------------
# Impact = exposure × realized volatility
df["shock_impact"] = df["exposure"] * df["volatility"]

# -----------------------------
# AVERAGE IMPACT BY SHOCK TYPE
# -----------------------------
impact_stats = (
    df[df["shock"] != 0]
    .groupby(["stock", "shock"])["shock_impact"]
    .mean()
    .unstack()
    .reset_index()
    .rename(columns={
        1: "avg_positive_impact",
       -1: "avg_negative_impact"
    })
)

impact_stats = impact_stats.fillna(0)

# -----------------------------
# COMPUTE ASYMMETRY
# -----------------------------
impact_stats["asymmetry_score"] = (
    impact_stats["avg_positive_impact"]
    - impact_stats["avg_negative_impact"]
)

impact_stats = impact_stats.sort_values(
    "asymmetry_score", ascending=False
)

impact_stats.to_csv(
    "phase4_firm_level_asymmetry.csv",
    index=False
)

print("✅ Phase 4 fixed: magnitude-based asymmetry computed")
print(impact_stats.head(10))
