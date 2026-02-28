# 📈 Financial Risk Propagation & Asymmetry Network

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-150458.svg)](https://pandas.pydata.org/)
[![NetworkX](https://img.shields.io/badge/NetworkX-Graph%20Analysis-005b96.svg)](https://networkx.org/)

An advanced pipeline for analyzing **risk propagation** and **volatility asymmetry** in financial markets using dynamic correlation networks. This project identifies how financial shocks spread through the market and which specific firms, sectors, or market communities drive systemic asymmetric impact.

## 💼 Business Context

### Problem Statement
Financial markets are highly interconnected ecosystems where local, idiosyncratic shocks (like a sudden drop in a single stock's price) can rapidly propagate, leading to widespread systemic instability. Traditional financial risk models often assume symmetrical shock impacts (i.e., treating positive and negative shocks equally) and rely on static covariance matrices. This fails to capture the true, dynamic nature of market stress, where negative shocks are often amplified by herd behavior, correlated sell-offs, and forced liquidations. These conditions create hidden vulnerabilities that are critical for portfolio managers, regulators, hedge funds, and risk analysts to understand dynamically.

### The Solution: Network Graph Theory
This project introduces a **Dynamic Financial Network Analysis Engine** to overcome the limitations of classical risk models. By treating the stock market as an evolving graph of correlations:
1.  **Dynamic Monitoring:** Captures 60-day rolling Pearson correlations to map the real-time structure of the market, acknowledging that relationships between equities change drastically during crisis regimes compared to bull markets.
2.  **Asymmetric Risk Profiling:** Uniquely separates the impact of positive vs. negative volatility shocks, assigning an **Asymmetry Score** to every firm and sector based on their specific directional behavior.
3.  **Actionable Intelligence:** Identifies "Amplifiers" (firms/sectors that worsen market drops) and "Stabilizers" (firms/sectors that absorb shocks and exhibit lower network connectivity during crashes), providing critical insights for risk mitigation, hedging strategies, and portfolio construction.

## ✨ Key Features & Methodologies
- **Volatility Shock Detection**: Employs rolling 20-day standard deviation distributions to statistically identify and isolate 5% high/low extreme market shocks, enabling event-based network analysis rather than continuous analysis.
- **Dynamic Sparse Network Construction**: Builds daily rolling correlation networks to measure interactions. Employs a specific correlation cutoff (e.g., ≥ 0.3) to isolate only strong, statistically significant relationships, thereby drastically reducing graph noise and isolating structural significance.
- **Systemic Risk Spillover Profiling**: Quantifies the total baseline network spillover, calculating the absolute sum of all weighted network dependencies, and benchmarks changes in systemic topology between 'Normal' background states vs. aggregated 'Shock' regimes.
- **Firm-Level Signed Asymmetry Scoring**: Calculates shock-weighted impacts, scoring individual firms based on their distinct behavior under positive vs. negative shocks, preserving the *sign* of the network relationship. 
- **Unsupervised Community & Sector Detection**: Highlights market substructures using the graph-theoretical **Louvain Community Detection heuristic** to group mathematically correlated equities irrespective of their nominal market sector. Contrasts these statistical communities with baseline NSE sectors to evaluate sector structural composition.

## 📊 Analytics & Metrics Output

The entire data pipeline yields granular, actionable datasets and visualizations based on these primary indicators:
*   **Total Network Spillover (Normal vs Shock):** Measures the absolute sum of all topological network weights (correlations) over time. Typically, the system demonstrates a substantial, alarming percentage increase in connectedness during shock regimes ("When the market crashes, all correlations go to 1").
*   **Signed Shock Impact:** Calculated for every node as `Network Exposure (signed sum of correlations) × Realized Nodes' Volatility`.
*   **Asymmetry Score:** Formally mathematically defined as `(Average Impact during Positive Shocks) - (Average Impact during Negative Shocks)`. 
    *   **Amplifiers:** Higher positive scores indicate firms that mathematically worsen market sell-offs due to a combination of high native volatility and powerful dense negative market network connections.
    *   **Stabilizers:** Scores closing on zero or becoming deeply negative suggest market stabilizers that absorb systemic pressure and decouple from overarching market drops. 
*   **Community / Sector Resilience Mapping:** Averages the underlying node-level asymmetry scores to bubble up macro-level systemic vulnerabilities. Evaluating average vulnerability by industry (e.g., IT, Banking, FMCG) or algorithmically detected Louvain communities highlights which sections of the market must be aggressively hedged during macroeconomic shocks.

## 🏗️ Detailed Pipeline Architecture

The analysis is broken down into 5 heavily structured, modular, independent Python phases:

### Phase 1: Data Processing & Statistical Shock Labeling
(`phase1_data_processing.py`)
- Standardizes financial time-series panel data (`stocks_df.csv`).
- Computes daily logarithmic returns: `return_t = ln(close_t) - ln(close_t-1)`.
- Re-runs continuous volatility modeling using a 20-day rolling standard deviation.
- Determines the individual volatility distribution per firm and categorizes real market shocks into binary labels based on percentiles:
  - `(1)` Positive Volatility Extremes: The Top 95th percentile.
  - `(-1)` Negative Volatility Extremes: The Bottom 5th percentile.

### Phase 2: Dynamic Sparse Network Construction
(`phase2_build_network.py` & `phase2_build_network_event_based.py`)
- Calculates a 60-day rolling Pearson correlation array, mandating a rigorous minimum of 50 exact overlapping active data points to omit spurious early-IPO or sparse data anomalies.
- Hard filters all continuous graph edges using a strict threshold parameter (Absolute Correlation ≥ 0.3).
- Binarizes normal and event-driven data groups to dump fully reconstructed daily graph Adjacency Matrices mapping to node mappings.

### Phase 3: Risk Propagation Baseline Quantification 
(`phase3_risk_propagation_baseline.py`)
- Iterates over daily Adjacency Matrices and analyzes the absolute total link degree (Total Market Connectedness).
- Groups edge lists strictly by the Phase 1 volatility labels to generate total Spillover visualizations proving structural disparity between normal baseline trading and identified systemic volatile shocks.

### Phase 4: Firm-Level Asymmetry
(`phase4_firm_level_asymmetry_signed.py` & `phase4_firm_level_asymmetry.py`)
- Computes node centrality degrees matching individual financial records but retaining the mathematical sign.
- Evaluates raw impact weights against the volatility bounds.
- Runs aggregation over distinct identified shock events to derive the core target variable: The normalized **Asymmetry Score**. 
- Exports full `phase4_firm_level_asymmetry_signed.csv` mapping every analyzed equity to its Stabilizer/Amplifier ranking.

### Phase 5: Network Communities, Sectors & Macro-Asymmetry
(`phase5_network_communities.py`, `phase5_sector_level_asymmetry.py`, `build_company_sector.py`)
- Maps underlying constituent stock tickers to known NSE index mappings (like Nifty Bank, Nifty IT, Nifty Pharma).
- Extracts static average node representations and applies the recursive Louvain Algorithm modularity optimizer. The optimizer strictly clusters highly internally dense and externally sparse groups of equities to prove un-documented mathematical market subsections.
- Bubbles up micro-network results to evaluate total macro market vulnerability.
- Auto-generates distribution visualizers contrasting Louvain sub-groups with classical Nifty groupings based on their averaged Asymmetry Score.

## 🚀 Environment Setup & Initial Execution

### Prerequisites

Ensure you have highly updated Python `3.8+` running. Standard dependency practices dictate utilizing an isolated virtual environment. 

1. **Clone & Setup the Environment**
```bash
python -m venv .venv
# On macOS/Linux shells:
source .venv/bin/activate  
# On Windows CMD/Powershell: 
.venv\Scripts\activate
```

2. **Install Network Analysis Dependencies**
```bash
pip install pandas numpy matplotlib networkx python-louvain
```

### Execution Flow

The full pipeline parses billions of edge interactions locally using highly optimized pandas vectorized chunks and networkx representations. You must ensure you pre-load your raw financial data in a `data/` subdirectory or matching local mappings with fields for ticker names, dates, and historical close limits. 

```bash
# Generate the basic sector mapping from indexes
python build_company_sector.py

# Detect anomalies and label extremes
python phase1_data_processing.py

# Roll correlations and establish sparse matrices
python phase2_build_network.py

# Compute base risk spillover differences
python phase3_risk_propagation_baseline.py

# Derive key Firm-Level Metrics
python phase4_firm_level_asymmetry_signed.py

# Aggregate Upward to Base Sectors
python phase5_sector_level_asymmetry.py

# Cluster unsupervised macro-communities
python phase5_network_communities.py
```

*Outputs, including structural summaries, plots, and CSV datasets, will automatically parse and save to the core repository root directly mapped to the designated input features.*

## 🔮 Future Architecture (Graph Embeddings)
The resulting arrays, adjacency snapshots (`phase2_shock_network.csv`) and engineered node features (`phase4_firm_level_asymmetry.csv`) generated by this methodology act as heavily optimized, standardized, and normalized foundational datasets for supervised **Graph Neural Network (GNN)**, and Long Short-Term Memory (LSTM) time-series evaluation targets for deep learning.

---
*Built to shed light on complex market dynamics mathematically, establishing data-driven insight into hidden localized systemic market risks.*
