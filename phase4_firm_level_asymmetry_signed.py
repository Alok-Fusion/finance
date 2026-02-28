import pandas as pd
import numpy as np

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("phase1_clean_shock_data.csv")
shock_net = pd.read_csv("phase2_shock_network.csv")

# =============================
# COMPUTE SIGNED NETWORK EXPOSURE
# =============================
signed_exposure = {}

for _, row in shock_net.iterrows():
    i, j, w = row["stock_i"], row["stock_j"], row["correlation"]  # KEEP SIGN

    signed_exposure[i] = signed_exposure.get(i, 0) + w
    signed_exposure[j] = signed_exposure.get(j, 0) + w

signed_exposure_df = pd.DataFrame(
    signed_exposure.items(),
    columns=["stock", "signed_exposure"]
)

# =============================
# MERGE INTO MAIN DATA
# =============================
df = df.merge(signed_exposure_df, on="stock", how="left").fillna(0)

# =============================
# COMPUTE SIGNED SHOCK IMPACT
# =============================
# Impact now reflects amplification (+) or stabilization (-)
df["signed_shock_impact"] = df["signed_exposure"] * df["volatility"]

# =============================
# AVERAGE BY SHOCK TYPE
# =============================
impact_stats = (
    df[df["shock"] != 0]
    .groupby(["stock", "shock"])["signed_shock_impact"]
    .mean()
    .unstack()
    .reset_index()
    .rename(columns={
        1: "avg_positive_impact",
       -1: "avg_negative_impact"
    })
)

impact_stats = impact_stats.fillna(0)

# =============================
# SIGNED ASYMMETRY
# =============================
impact_stats["asymmetry_score"] = (
    impact_stats["avg_positive_impact"]
    - impact_stats["avg_negative_impact"]
)

impact_stats = impact_stats.sort_values(
    "asymmetry_score", ascending=False
)

impact_stats.to_csv(
    "phase4_firm_level_asymmetry_signed.csv",
    index=False
)

print("✅ Phase 4 (SIGNED) complete")
print("\nTop amplifiers:")
print(impact_stats.head(5))

print("\nTop stabilizers:")
print(impact_stats.tail(5))
