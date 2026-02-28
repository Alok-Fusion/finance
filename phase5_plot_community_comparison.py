import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# =============================
# LOAD COMMUNITY DATA
# =============================
df = pd.read_csv("phase5_community_asymmetry.csv")

# Sort by asymmetry for clean plotting
df = df.sort_values("avg_asymmetry", ascending=False)

communities = df["community"].astype(str)

# =============================
# BAR POSITIONS
# =============================
x = np.arange(len(communities))
width = 0.25

# =============================
# PLOT
# =============================
fig, ax = plt.subplots(figsize=(8, 4))

ax.bar(
    x - width,
    df["avg_positive_impact"],
    width,
    label="Avg Positive Impact",
    color="#22c55e"
)

ax.bar(
    x,
    df["avg_negative_impact"],
    width,
    label="Avg Negative Impact",
    color="#ef4444"
)

ax.bar(
    x + width,
    df["avg_asymmetry"],
    width,
    label="Avg Asymmetry",
    color="#3b82f6"
)

# -----------------------------
# AXES & LABELS
# -----------------------------
ax.axhline(0, color="black", linewidth=0.8)
ax.set_xticks(x)
ax.set_xticklabels(communities)
ax.set_xlabel("Community ID")
ax.set_ylabel("Impact Measure")
ax.set_title("Community-Level Asymmetric Risk Response")

ax.legend(frameon=False)
plt.tight_layout()
plt.show()
