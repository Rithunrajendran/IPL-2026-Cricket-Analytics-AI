# IPL 2026 Cricket Analytics Platform

A full-stack cricket analytics project built on IPL 2026 ball-by-ball data. Covers the complete data pipeline from raw JSON through Python analytics, SQL, Excel, Power BI, machine learning, and a live interactive Streamlit web application.

**Live App:** [IPL 2026 Cricket Analytics Platform](https://rithunrajendran-ipl-2026-cricket-analytics-platform-streamlit-app.streamlit.app)

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data Processing | Python, Pandas, NumPy |
| Database | MySQL, SQL Views, CTEs, Window Functions |
| Visualisation | Power BI, Excel, Plotly |
| Machine Learning | Scikit-learn, Random Forest |
| Web Application | Streamlit |

---

## Project Architecture

```text
Cricsheet IPL 2026 JSON
         │
         ▼
  Python Data Pipeline
  (extraction · cleaning · validation)
         │
         ├──► processed/ CSV files
         │
         ├──► MySQL Analytics Warehouse
         │         └── 10 Analytical Views
         │
         ├──► Excel Business Analysis
         │
         ├──► Power BI Dashboard
         │
         ├──► Random Forest Match Predictor
         │
         └──► Streamlit Web Application
```

---

## Dataset

| Metric | Value |
|---|---|
| Source | Cricsheet IPL JSON |
| Season | IPL 2026 |
| Matches (completed) | 72 |
| Ball-by-ball deliveries | 17,527 |
| Teams | 10 |
| Venues | 13 |
| Unique batters | 176 |
| Unique bowlers | 125 |

Two matches excluded from ML — 1 No Result (KKR vs PBKS) and 1 Tie (KKR vs LSG).

---

## Streamlit Application

The web app has 8 sections accessible from the sidebar:

### 1. Overview
Season dashboard with a KPI strip (matches, runs, teams, players, wickets, sixes), team run totals and win % charts, and season highlights (Orange Cap, Purple Cap, Champions).

### 2. Team Performance
- **Season Overview** — wins bar chart and runs scored vs conceded scatter
- **Team Deep-Dive** — win gauge, run breakdown, and phase-wise performance for any team
- **Head to Head** — side-by-side comparison of any two teams

### 3. Player Analysis
- **Leaderboard** — filter by balls faced, sort by runs / strike rate / sixes / fours / boundary %
- **Player Profile** — batting percentile radar, milestone scores, and bowling stats for all-rounders

### 4. Bowling Stats
- **Leaderboard** — filter by wickets, sort by economy / average / strike rate / hauls
- **Bowler Profile** — economy gauge and wicket haul breakdown (3W+, 4W+, 5W+)

### 5. Venue Analysis
- Average match scores and chase success rates across all grounds
- Per-venue deep-dive with chase success gauge and match summary

### 6. Match Explorer
- Run distribution and results breakdown across all 74 matches
- Per-match innings comparison and full result details

### 7. Data Explorer
Query the dataset through pre-built questions — no code needed. Pick a category (Team, Batting, Bowling, Phase, Venue, Match, Comparison), choose a question, and results render instantly as a chart or metric.

### 8. Match Prediction
Select two teams and predict the winner using the trained Random Forest model. Shows win probability gauges for both teams.

### Run Locally

```bash
git clone https://github.com/rithunrajendran/IPL-2026-Cricket-Analytics-Platform.git
cd IPL-2026-Cricket-Analytics-Platform
pip install -r requirements.txt
streamlit run streamlit/app.py
```

---

## Machine Learning

**Objective:** Predict match winner (binary classification — Team 1 wins or not)

**Model:** Random Forest (selected after comparing 4 models)

| Model | CV Accuracy | Std Dev |
|---|---|---|
| Random Forest | **57.62%** | 12.47% |
| Extra Trees | 56.50% | 11.91% |
| Logistic Regression | 53.16% | 12.12% |
| Gradient Boosting | 52.82% | 9.12% |

**Features (13):**
`team1`, `team2`, `venue`, `team1_prev_win_pct`, `team2_prev_win_pct`, `team1_recent_form`, `team2_recent_form`, `team1_avg_runs`, `team2_avg_runs`, `team1_avg_conceded`, `team2_avg_conceded`, `toss_winner_is_team1`, `toss_decision`

Historical features are calculated chronologically — no data leakage from future matches.

> **Note:** 57.6% accuracy reflects a single-season dataset of 72 matches. T20 outcomes are inherently hard to predict; this is an experimental baseline.

---

## Analytics Produced

| Area | Key Metrics |
|---|---|
| Batting | Runs, SR, 4s, 6s, boundary %, dot %, 30+/50+/100+ scores |
| Bowling | Wickets, economy, SR, average, 3W+/4W+/5W+ hauls |
| Team | Matches, wins, losses, win %, runs scored/conceded |
| Phase | Powerplay / Middle / Death — runs, wickets, run rate |
| Venue | Avg scores, chase success %, highest match score |
| Match | Innings scores, result type, margins |
| Partnership | 921 innings across 405 unique partnerships |
| Turning Points | Over-level momentum and wicket impact |
| Player Impact | Combined batting + bowling impact scores |

### Top Run Scorers (IPL 2026)

| Player | Runs |
|---|---|
| V Suryavanshi | 776 |
| Shubman Gill | 732 |
| B Sai Sudharsan | 722 |
| V Kohli | 675 |
| H Klaasen | 624 |

---

## SQL Analytics Layer

Database: `ipl_analytics`

**Tables:** `matches_2026`, `deliveries_2026`

**Views:**
`vw_match_analytics` · `vw_venue_performance` · `vw_team_performance` · `vw_batting_performance` · `vw_bowling_performance` · `vw_phase_performance` · `vw_toss_impact` · `vw_match_results` · `vw_head_to_head` · `vw_chasing_vs_defending`

Concepts demonstrated: JOINs, GROUP BY, CASE, CTEs, aggregations, window functions, ranking, conditional calculations.

---

## Project Structure

```text
IPL-2026-Cricket-Analytics-Platform/
│
├── cricsheet_json/          # Raw IPL 2026 source JSON files
├── processed/               # Generated CSV analytics datasets
│   ├── matches_2026.csv
│   ├── deliveries_2026.csv
│   ├── batting_metrics_2026.csv
│   ├── bowling_metrics_2026.csv
│   ├── team_metrics_2026.csv
│   ├── phase_metrics_2026.csv
│   ├── match_analytics_2026.csv
│   ├── venue_analytics_2026.csv
│   ├── player_impact_2026.csv
│   ├── bowling_impact_2026.csv
│   ├── partnership_analytics_2026.csv
│   ├── match_turning_points_2026.csv
│   └── team_phase_analysis_2026.csv
│
├── models/
│   └── ipl_2026_final_random_forest.pkl
│
├── python/                  # Data pipeline scripts (01 → 23)
├── streamlit/
│   └── app.py               # Streamlit web application
├── MS EXCEL/
│   └── IPL_2026_Analytics.xlsx
├── POWERBI/
│   └── IPL_2026_Analytics_Dashboard.pbix
│
├── DATA_DICTIONARY.md
├── requirements.txt
└── README.md
```

---

## Key Outcomes

This project demonstrates end-to-end experience with:

- Python data engineering and cleaning
- SQL analytical layer design
- Excel and Power BI business reporting
- Machine learning model comparison and selection
- Chronological feature engineering (no data leakage)
- Interactive web application development with Streamlit
- Full project documentation and deployment
