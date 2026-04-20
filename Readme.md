# Credit Card Campaign Analytics

## Project Overview
A end-to-end data analytics project simulating a real banking 
environment where a marketing team runs credit card campaigns 
across multiple customer segments. The goal is to help bank 
marketing managers make smarter budget decisions by analyzing 
which campaigns actually generate returns — not just conversions.

Key business finding: a campaign with the highest conversion rate 
ranked last in revenue, proving that conversion rate alone is a 
misleading optimization metric. Premium customers (5.6% of base) 
generated 75% of total revenue, making segment-level targeting 
the most impactful lever for campaign ROI.

## Problem Statement
Banks run multiple marketing campaigns simultaneously with limited 
budgets. Without proper analytics, budget gets allocated based on 
conversion rate — which is misleading. This project builds a 
complete analytics system to identify which campaigns and customer 
segments deliver real business value measured by ROI.

## Tech Stack
| Tool | Purpose |
|---|---|
| Python (pandas, numpy) | Data generation, cleaning, analysis |
| Matplotlib / Seaborn | Data visualization |
| SQL (SQLite) | KPI computation, campaign ranking |
| Git / GitHub | Version control |


## Project Architecture
Raw Data (CSV)
↓
SQL Layer (KPIs — conversion, revenue, ROI, ranking)
↓
Python Layer (EDA, trends, segment analysis, charts)
↓
Insights + Recommendations

## Dataset
Synthetic dataset generated using Python to mirror real banking 
distributions. Banking data is not publicly available due to privacy 
regulations — synthetic generation allowed full control over 
realistic distributions.

| Table | Rows | Description |
|---|---|---|
| customers | 2,000 | Age, income, city, segment |
| campaigns | 20 | Type, budget, duration |
| transactions | 5,000 | Amount, date per customer |
| campaign_responses | 2,897 | Conversion per campaign |

Key design decisions:
- Income modeled using lognormal distribution (right-skewed — 
  mirrors real income data)
- 4.4% missing income values injected to simulate real-world noise
- Conversion rates vary by segment (Premium 30%, Mass 12%) 
  to encode realistic business behavior

## Key Findings
1. **Conversion rate is misleading** — C014 ranked #1 in conversion 
   but #20 in revenue
2. **Email campaigns deliver best ROI** — top 3 ROI campaigns all 
   Email, lowest budgets, highest returns
3. **Telemarketing consistently underperforms** — bottom 4 ROI 
   positions despite highest budgets
4. **Premium segment drives 75% revenue** — from only 5.6% 
   of customers
5. **Revenue peaks in October** — February weakest month, 
   strongest candidate for campaign push
6. **ROI figures reflect synthetic scale** — relative rankings 
   across campaigns remain valid for business decisions

## How to Run
```bash
# 1. Clone the repo
git clone https://github.com/Siddhantkatare/credit-card-campaign-analytics.git

# 2. Install dependencies
pip install pandas numpy faker matplotlib seaborn jupyter

# 3. Generate dataset
python generate_data.py

# 4. Load into database
python load_to_db.py

# 5. Open analysis notebook
jupyter notebook notebooks/analysis.ipynb
```

## Project Structure
credit-card-campaign-analytics/
├── data/                    ← generated CSVs (gitignored)
├── sql/                     ← 7 SQL queries with comments
├── notebooks/
│   ├── analysis.ipynb       ← full Python analysis
│   └── charts/              ← 4 visualization outputs
├── insights.md              ← business findings document
├── generate_data.py         ← synthetic data generation
├── load_to_db.py            ← CSV to SQLite loader
└── README.md

## Skills Demonstrated
- Relational database design and SQL window functions
- Synthetic data engineering with realistic distributions
- Exploratory data analysis and visualization
- Business insight generation from raw data
- End-to-end project structure and documentation