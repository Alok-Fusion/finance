import pandas as pd

# =============================
# LOAD NSE INDEX DATA
# =============================
df = pd.read_csv("./data/nse_indexes.csv")

# Normalize column names
df.columns = df.columns.str.lower().str.strip()

print("Detected columns:", df.columns.tolist())

# -----------------------------
# DETECT REQUIRED COLUMNS
# -----------------------------
# index name column
if "index name" in df.columns:
    index_col = "index name"
elif "index" in df.columns:
    index_col = "index"
elif "index_name" in df.columns:
    index_col = "index_name"
else:
    raise ValueError("❌ Cannot find index name column")

# constituents column
if "constituents" in df.columns:
    cons_col = "constituents"
elif "stocks" in df.columns:
    cons_col = "stocks"
elif "symbols" in df.columns:
    cons_col = "symbols"
else:
    raise ValueError("❌ Cannot find constituents column")

# -----------------------------
# MAP INDEX → SECTOR
# -----------------------------
index_sector_map = {
    "nifty it": "IT",
    "nifty bank": "Banking",
    "nifty fmcg": "FMCG",
    "nifty auto": "Auto",
    "nifty energy": "Energy",
    "nifty metal": "Metals",
    "nifty pharma": "Pharma",
    "nifty realty": "Realty",
    "nifty fin service": "Finance"
}

rows = []

for _, row in df.iterrows():
    index_name = str(row[index_col]).lower().strip()

    if index_name not in index_sector_map:
        continue

    sector = index_sector_map[index_name]
    companies = str(row[cons_col]).split("|")

    for c in companies:
        rows.append({
            "company": c.strip(),
            "sector": sector
        })

company_sector = (
    pd.DataFrame(rows)
    .drop_duplicates()
    .sort_values(["company", "sector"])
)

company_sector.to_csv("company_sector.csv", index=False)

print("✅ company_sector.csv created successfully")
print(company_sector.head(20))
