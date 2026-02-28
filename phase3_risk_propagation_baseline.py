import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# =============================
# LOAD DATA
# =============================
df = pd.read_csv("phase1_clean_shock_data.csv")
normal_net = pd.read_csv("phase2_normal_network.csv")
shock_net  = pd.read_csv("phase2_shock_network.csv")

# -----------------------------
# BUILD ADJACENCY
# -----------------------------
def compute_exposure(network_df):
    exposure = {}

    for _, row in network_df.iterrows():
        i, j, w = row["stock_i"], row["stock_j"], abs(row["weight"])

        exposure[i] = exposure.get(i, 0) + w
        exposure[j] = exposure.get(j, 0) + w

    return exposure

normal_exposure = compute_exposure(normal_net)
shock_exposure  = compute_exposure(shock_net)

# =============================
# IDENTIFY SHOCKED STOCKS
# =============================
shocked_stocks = df[df["shock"] != 0]["stock"].unique()

# =============================
# TOTAL NETWORK SPILLOVER
# =============================
def total_network_spillover(network_df):
    return network_df["weight"].abs().sum()

normal_spill = total_network_spillover(normal_net)
shock_spill  = total_network_spillover(shock_net)

# =============================
# RESULTS
# =============================
result = pd.DataFrame({
    "Regime": ["Normal", "Shock"],
    "Total Spillover": [normal_spill, shock_spill]
})

result["Relative Increase (%)"] = (
    (shock_spill - normal_spill) / (normal_spill + 1e-6) * 100
)

print("\n📊 Baseline Risk Propagation")
print(result)

# -----------------------------
# SIMPLE SPILLOVER COMPARISON PLOT
# -----------------------------
fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(
    result["Regime"],
    result["Total Spillover"],
    color=["#3b82f6", "#ef4444"],
    alpha=0.8
)

ax.set_ylabel("Total Network Spillover")
ax.set_title("Risk Spillover: Normal vs Volatility Shock Regimes")

# Annotate bars
for i, v in enumerate(result["Total Spillover"]):
    ax.text(
        i,
        v * 1.01,
        f"{v:.0f}",
        ha="center",
        va="bottom",
        fontsize=9
    )

plt.tight_layout()
plt.show()
