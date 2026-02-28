# 📈 Financial Risk Propagation & Asymmetry Network

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph%20Analysis-005b96.svg)](https://networkx.org/)

An advanced pipeline for analyzing **risk propagation** and **volatility asymmetry** in financial markets using dynamic correlation networks. This project identifies how financial shocks spread through the market and which specific firms, sectors, or market communities drive systemic asymmetric impact.

## 💼 Business Context

### Problem Statement
Financial markets are highly interconnected ecosystems where local, idiosyncratic shocks (like a sudden drop in a single stock's price) can rapidly propagate, leading to widespread systemic instability. Traditional financial risk models often assume symmetrical shock impacts (i.e., treating positive and negative shocks equally) and rely on static correlations. This fails to capture the true, dynamic nature of market stress, where negative shocks are often amplified by herd behavior and forced liquidations, creating hidden vulnerabilities that are critical for portfolio managers, regulators, and risk analysts to understand.

### The Solution
This project introduces a **Dynamic Financial Network Analysis Engine**. By treating the stock market as an evolving graph of correlations:
1.  **Dynamic Monitoring:** Captures 60-day rolling correlations to map the real-time structure of the market.
2.  **Asymmetric Risk Profiling:** Uniquely separates the impact of positive vs. negative volatility shocks, assigning an **Asymmetry Score** to every firm and sector. 
3.  **Actionable Intelligence:** Identifies "Amplifiers" (firms/sectors that worsen market drops) and "Stabilizers" (firms/sectors that absorb shocks), providing critical insights for risk mitigation, hedging strategies, and portfolio construction.

## ✨ Key Features
- **Volatility Shock Detection**: Employs rolling volatility to identify 5% high/low extreme market shocks.
- **Dynamic Network Construction**: Builds rolling correlation networks to measure interactions between stocks over time.
- **Systemic Risk Spillover**: Quantifies total baseline network spillover, comparing 'Normal' vs. 'Shock' regimes.
- **Firm-Level Asymmetry Scoring**: Calculates shock-weighted impacts, scoring individual firms based on their distinct behavior under positive vs. negative shocks.
- **Community & Sector Detection**: Highlights market substructures (via Louvain community detection) that disproportionately absorb or propagate risk.

## 📊 Analytics & Metrics Output

The pipeline generates several key metric outputs:
*   **Total Spillover (Normal vs Shock):** Measures the absolute sum of all network correlations. Typically demonstrates a substantial percentage increase during shock regimes.
*   **Signed Shock Impact:** Calculated as `Network Exposure (signed sum of correlations) × Realized Volatility`.
*   **Asymmetry Score:** Defined as `Average Impact during Positive Shocks - Average Impact during Negative Shocks`. Higher positive scores indicate firms that amplify volatility.
*   **Community / Sector Resilience:** Averages the firm-level asymmetry scores grouping by industry (e.g., IT, Banking, FMCG) or algorithmically detected Louvain communities, revealing macro-level market structural risks.

## 🏗️ Pipeline Architecture

The analysis is broken down into structured, independent phases:

### Phase 1: Data Processing & Shock Labeling
(`phase1_data_processing.py`)
- Standardizes financial panel data.
- Computes log returns and 20-day rolling volatility.
- Identifies and labels the top 5% (high) and bottom 5% (low) volatility periods as real market shocks.

### Phase 2: Dynamic Network Construction
(`phase2_build_network.py` & `phase2_build_network_event_based.py`)
- Calculates a 60-day rolling correlation matrix.
- Filters edges using a specific correlation threshold (e.g., ≥ 0.3) to build daily interconnected market networks requiring a minimum of 50 overlapping observations.

### Phase 3: Risk Propagation Baseline
(`phase3_risk_propagation_baseline.py`)
- Determines system-wide exposure by aggregating link weights (correlations).
- Computes and visually compares total network spillover between normal and volatile regimes.

### Phase 4: Firm-Level Asymmetry
(`phase4_firm_level_asymmetry_signed.py`)
- Weighs a firm's network exposure by its realized volatility, preserving the network sign (amplification vs. stabilization).
- Distinguishes the average impact during positive and negative shocks.
- Generates an `asymmetry_score` to isolate asymmetrical risk contributors (identifying Top Amplifiers and Top Stabilizers).

### Phase 5: Network Communities & Sector Asymmetry
(`phase5_network_communities.py`, `phase5_sector_level_asymmetry.py`, `build_company_sector.py`)
- Maps constituent stocks from NSE indices (like Nifty Bank, Nifty IT) to define sectors.
- Applies Louvain Community Detection to uncover clusters of highly correlated stocks on the graph.
- Aggregates firm-level asymmetry upward, assessing which sectors or underlying market communities drive systemic fragility.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3 installed. Create a virtual environment and install the required packages:

```bash
python -m venv .venv
# On Mac/Linux:
source .venv/bin/activate  
# On Windows: 
.venv\Scripts\activate

pip install pandas numpy matplotlib networkx python-louvain
```

### Execution

Run the phases sequentially to execute the full data pipeline. Store your raw daily stock data inside `data/stocks_df.csv` and index constituents in `data/nse_indexes.csv` before beginning.

```bash
python build_company_sector.py
python phase1_data_processing.py
python phase2_build_network.py
python phase3_risk_propagation_baseline.py
python phase4_firm_level_asymmetry_signed.py
python phase5_sector_level_asymmetry.py
python phase5_network_communities.py
```

*Outputs, including statistical summaries and CSV datasets, will automatically save to the repository root.*

---
*Built to shed light on complex market dynamics and hidden systemic risks.*
