import pandas as pd
import networkx as nx
import numpy as np

# =============================
# LOAD DATA
# =============================
firm_df = pd.read_csv("phase4_firm_level_asymmetry_signed.csv")
edge_df = pd.read_csv("phase2_shock_network.csv")

# -----------------------------
# BUILD GRAPH
# -----------------------------
G = nx.Graph()

for _, row in edge_df.iterrows():
    G.add_edge(
        row["stock_i"],
        row["stock_j"],
        weight=abs(row["correlation"])
    )

# -----------------------------
# COMMUNITY DETECTION (Louvain)
# -----------------------------
try:
    import community.community_louvain as community_louvain
except ImportError:
    raise ImportError("Install python-louvain: pip install python-louvain")

partition = community_louvain.best_partition(G, weight="weight")

# Convert to DataFrame
community_df = pd.DataFrame.from_dict(
    partition, orient="index", columns=["community"]
).reset_index().rename(columns={"index": "stock"})

# -----------------------------
# MERGE WITH ASYMMETRY
# -----------------------------
merged = firm_df.merge(community_df, on="stock", how="inner")

# -----------------------------
# COMMUNITY-LEVEL AGGREGATION
# -----------------------------
community_summary = (
    merged
    .groupby("community")
    .agg(
        avg_positive_impact=("avg_positive_impact", "mean"),
        avg_negative_impact=("avg_negative_impact", "mean"),
        avg_asymmetry=("asymmetry_score", "mean"),
        firm_count=("stock", "count")
    )
    .reset_index()
    .sort_values("avg_asymmetry", ascending=False)
)

# -----------------------------
# SAVE OUTPUT
# -----------------------------
merged.to_csv("phase5_firm_with_communities.csv", index=False)
community_summary.to_csv("phase5_community_asymmetry.csv", index=False)

print("✅ Phase 5 complete: Network communities identified")
print("\nCommunity-level asymmetric impact:")
print(community_summary)
