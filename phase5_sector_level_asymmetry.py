import pandas as pd
import numpy as np

# =============================
# LOAD DATA
# =============================
firm_asym = pd.read_csv("phase4_firm_level_asymmetry_signed.csv")
sector_map = pd.read_csv("company_sector.csv")  # stock, sector

# -----------------------------
# MERGE SECTOR INFO
# -----------------------------
df = firm_asym.merge(
    sector_map,
    left_on="stock",
    right_on="company",
    how="left"
)

# Drop firms without sector info (if any)
df = df.dropna(subset=["sector"])

# =============================
# SECTOR-LEVEL AGGREGATION
# =============================
sector_df = (
    df.groupby("sector")
      .agg(
          avg_asymmetry=("asymmetry_score", "mean"),
          median_asymmetry=("asymmetry_score", "median"),
          firm_count=("stock", "count")
      )
      .reset_index()
)

# Sort by average asymmetry
sector_df = sector_df.sort_values(
    "avg_asymmetry", ascending=False
)

sector_df.to_csv(
    "phase5_sector_level_asymmetry.csv",
    index=False
)

print("📊 Phase 5 complete: sector-level signed asymmetry")
print(sector_df)
