import pandas as pd
import matplotlib.pyplot as plt

# Load data
df = pd.read_csv("phase5_community_asymmetry.csv")

# Sort by asymmetry
df = df.sort_values("avg_asymmetry", ascending=False)

# Plot
plt.figure(figsize=(7, 4))

colors = ["#ef4444" if x > 0 else "#22c55e" for x in df["avg_asymmetry"]]

plt.bar(
    df["community"].astype(str),
    df["avg_asymmetry"],
    color=colors
)

plt.axhline(0, color="black", linewidth=0.8)
plt.xlabel("Network Community")
plt.ylabel("Asymmetric Risk Impact")
plt.title("Asymmetric Risk Propagation Across Network Communities")

plt.tight_layout()
plt.show()
