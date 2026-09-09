# IPL 2026 – End-to-End Cricket Analytics & AI Intelligence Platform

## 1. Project Overview

This project is an end-to-end cricket analytics platform built using IPL 2026 ball-by-ball data.

The project transforms raw cricket data into:
- Clean analytical datasets
- SQL-based analytics and views
- Excel business analysis
- Power BI dashboards
- Match outcome prediction using Machine Learning
- A local RAG-style analytics assistant that retrieves grounded IPL statistics and generates natural-language answers

### End-to-End Architecture

```text
Cricsheet IPL JSON
       │
       ▼
Python Data Extraction & Cleaning
       │
       ├── Match-level data
       └── Ball-by-ball delivery data
       │
       ▼
Python Analytics & Feature Engineering
       │
       ├── Batting metrics
       ├── Bowling metrics
       ├── Team metrics
       ├── Phase metrics
       ├── Venue analytics
       ├── Player impact
       ├── Partnership analytics
       └── Match turning points
       │
       ├──────────────► MySQL Analytics Warehouse
       │                     │
       │                     └── Analytical Views
       │
       ├──────────────► Excel Business Analysis
       │
       └──────────────► Power BI Dashboard

       Historical Match Data
              │
              ▼
       Feature Engineering
              │
              ▼
       Random Forest
              │
              ▼
       Match Prediction

       Analytics CSVs
              │
              ▼
       Retrieval Layer
              │
              ▼
       Grounded Context
              │
              ▼
       Local RAG Analytics Assistant
```

---

## 2. Business Objective

The objective is to build a reusable cricket analytics solution that can answer business-style questions such as:

- Which teams performed best?
- Who were the leading run scorers?
- Who were the leading wicket takers?
- Which venues produced high-scoring matches?
- How did teams perform across Powerplay, Middle and Death phases?
- How successful were chasing teams?
- What impact did the toss have?
- Which players had strong overall impact?
- Which team is more likely to win a future matchup based on historical features?
- Can an analytics assistant answer questions using only retrieved project data?

---

## 3. Dataset

### Source

Primary ball-by-ball source:
**Cricsheet – IPL JSON data**

The project filtered the source data to IPL 2026.

### Dataset Size

- Total JSON files available in downloaded IPL package: **1,243**
- IPL 2026 matches identified: **74**
- Ball-by-ball delivery records: **17,527**
- Teams: **10**
- Venues: **13**
- Unique batters in batting analytics: **176**
- Bowlers in bowling analytics: **125**

### Match Results

IPL 2026 data contains:
- **72 completed/decided matches**
- **1 No Result**
- **1 Tie**

The two matches without a normal winner were:
- KKR vs PBKS — No Result
- KKR vs LSG — Tie

For match-outcome ML, the dataset contains **72 usable completed matches**.

---

## 4. Technology Stack

### Programming
- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn

### Database
- MySQL
- MySQL Workbench
- SQL Views
- CTEs
- Window Functions

### Business Intelligence
- Microsoft Excel
- Power BI
- Power BI slicers and visualizations
- DAX knowledge can be extended with additional measures if required

### Machine Learning
- Scikit-learn
- Random Forest
- Extra Trees
- Logistic Regression
- Gradient Boosting
- Cross-validation

### AI / RAG
- Python retrieval layer
- Grounded context generation
- Local deterministic answer generation
- Designed so an LLM/API layer can be added later without changing the retrieval logic

---

## 5. Project Folder Structure

```text
IPL DATASET/
│
├── cricsheet_json/
│   └── IPL JSON source files
│
├── processed/
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
├── python/
│   ├── 01_inspect_data.py
│   ├── 02_inspect_json.py
│   ├── 03_find_2026.py
│   ├── 04_create_matches.py
│   ├── 05_inspect_2026_innings.py
│   ├── 06_create_deliveries.py
│   ├── 07_validate_data.py
│   ├── 07b_check_duplicates.py
│   ├── 07c_check_real_duplicates.py
│   ├── 07d_check_source_duplicates.py
│   ├── 07e_check_all_source_duplicates.py
│   ├── 07f_check_match_outcomes.py
│   ├── 08_batting_metrics.py
│   ├── 08_bowling_metrics.py
│   ├── 08_team_metrics.py
│   ├── 08_phase_metrics.py
│   ├── 08_batting_advanced.py
│   ├── 08_batting_milestones.py
│   ├── 08_bowling_advanced.py
│   ├── 08_validate_features.py
│   ├── 09_match_analytics.py
│   ├── 10_venue_analytics.py
│   ├── 11_player_impact.py
│   ├── 12_bowling_impact.py
│   ├── 13_partnership_analytics.py
│   ├── 14_match_turning_points.py
│   ├── 15_team_phase_analysis.py
│   ├── 16_ml_match_prediction.py
│   ├── 17_ml_improved_model.py
│   ├── 19_compare_models.py
│   ├── 20_train_final_model.py
│   ├── 21_predict_match.py
│   ├── 22_rag_retrieval.py
│   └── 23_rag_ai_assistant.py
│
├── IPL_2026_Analytics.xlsx
└── powerbi/
    └── IPL_2026_Analytics_Dashboard.pbix
```

---

## 6. Python Data Pipeline

### Step 1 – Inspect source data
The raw JSON structure was inspected to understand:
- Match metadata
- Teams
- Toss
- Outcome
- Innings
- Overs
- Deliveries
- Runs
- Extras
- Wickets

### Step 2 – Identify IPL 2026
All source files were scanned and the 2026 IPL season was isolated.

### Step 3 – Create match-level dataset

Output:

`processed/matches_2026.csv`

Important columns:
- match_id
- season
- match_date
- venue
- city
- team1
- team2
- toss_winner
- toss_decision
- winner
- result_type
- player_of_match

### Step 4 – Create delivery-level dataset

Output:

`processed/deliveries_2026.csv`

Important columns:
- match_id
- innings
- over
- actual_delivery
- batting_team
- batter
- bowler
- non_striker
- batter_runs
- extra_runs
- total_runs
- wides
- noballs
- byes
- legbyes
- penalty
- is_legal_delivery
- is_wicket
- dismissal_type
- player_dismissed

---

## 7. Data Validation

Validation was performed before downstream analytics.

Checks included:
- Match count
- Missing winners
- Missing player-of-match values
- Team count
- Missing core delivery fields
- Run distributions
- Extra distributions
- Wicket types
- Duplicate/source anomaly investigation

### Important Data Quality Finding

Some Cricsheet source innings contain repeated delivery records and delivery numbering can behave differently around illegal deliveries.

Instead of blindly deleting every repeated delivery, the source structure was investigated first.

For specific analytics where exact duplicate source rows could distort aggregation, exact duplicate rows were removed before aggregation.

This preserves traceability while avoiding inflated analytical metrics.

---

## 8. Core Analytics

### Batting

Calculated:
- Total runs
- Balls faced
- Strike rate
- Fours
- Sixes
- Boundary runs
- Boundary percentage
- Dot-ball percentage
- 30+ scores
- 50+ scores
- 100+ scores
- Highest score

Top run scorers included:
- V Suryavanshi — 776
- Shubman Gill — 732
- B Sai Sudharsan — 722
- V Kohli — 675
- H Klaasen — 624

### Bowling

Calculated:
- Wickets
- Runs conceded
- Legal balls
- Economy
- Bowling strike rate
- Dot-ball percentage
- Bowling average
- 3/4/5-wicket hauls
- Best match wickets

Important bowling rules:
- Bowler-credited dismissals include caught, bowled, LBW, caught and bowled, stumped and hit wicket.
- Run outs and other non-bowler dismissals are excluded from bowler wicket totals.
- Byes and leg-byes are excluded from bowler runs conceded.
- Wides and no-balls are included in runs conceded.

### Team Analytics

Calculated:
- Matches played
- Wins
- Losses
- Win percentage
- Runs scored
- Runs conceded

Example:
RCB played 16 matches, won 11 and lost 5, giving a **68.75% win percentage**.

### Phase Analytics

The innings were divided into:
- Powerplay
- Middle
- Death

Metrics:
- Runs
- Legal balls
- Wickets
- Run rate
- Wicket rate

### Match Analytics

Calculated:
- First innings score
- Second innings score
- Chasing/defending result
- Run margin
- Wicket margin
- Total match runs
- Match result type

Across the season:
- 45 matches were classified as chases
- 27 as defended totals
- 1 No Result
- 1 Tie

### Venue Analytics

Calculated:
- Matches played
- Average first innings score
- Average second innings score
- Average match runs
- Highest match score
- Chases won
- Matches defended
- Chase success percentage

### Player Impact

Combined scoring and milestone information to identify players with:
- High run totals
- High individual scores
- Frequent 30+ scores
- Frequent 50+ scores
- 100+ scores
- Ducks

### Partnership Analytics

Partnership combinations were analyzed across innings.

The analysis produced:
- **405 unique partnership combinations**
- **921 partnership innings**

Highest partnerships included:
- KL Rahul + N Rana — 220
- B Sai Sudharsan + Shubman Gill — 167
- Rickelton + Sharma — 148

### Match Turning Points

Over-level analytics were used to identify:
- High-scoring overs
- Wicket overs
- Over run rate
- Momentum patterns

### Team Phase Analysis

Teams were compared by:
- Powerplay performance
- Middle-over performance
- Death-over performance
- Runs
- Wickets
- Run rate
- Best scoring phase

---

## 9. MySQL Analytics Layer

Database:

`ipl_analytics`

Tables:
- `matches_2026`
- `deliveries_2026`

Views:
- `vw_match_analytics`
- `vw_venue_performance`
- `vw_team_performance`
- `vw_batting_performance`
- `vw_bowling_performance`
- `vw_phase_performance`
- `vw_toss_impact`
- `vw_match_results`
- `vw_head_to_head`
- `vw_chasing_vs_defending`

SQL concepts demonstrated:
- JOIN
- GROUP BY
- CASE
- CTE
- Aggregations
- Window functions
- Ranking
- Conditional calculations
- Analytical views

Example business question:

> Who are the top run scorers?

A window function can rank batters by total runs.

---

## 10. Excel Analysis

Workbook:

`IPL_2026_Analytics.xlsx`

Sheets:
1. Team Performance
2. Batting Performance
3. Bowling Performance
4. Venue Performance
5. Match Analytics
6. Phase Performance

Charts created:
- Wins by Team
- Runs Scored vs Runs Conceded
- Win Percentage by Team
- Top 10 Run Scorers
- Top 10 Wicket Takers
- Average Match Runs by Venue

The Excel workbook provides a business-friendly analytical layer before visualization in Power BI.

---

## 11. Power BI Dashboard

Dashboard file:

`powerbi/IPL_2026_Analytics_Dashboard.pbix`

Dashboard components:
- Total Matches KPI
- Total Runs KPI
- Top 10 Run Scorers
- Top 10 Wicket Takers
- Team Filter
- Wins by Team
- Win Percentage by Team
- Runs Scored vs Runs Conceded
- Runs by Phase
- Toss Decision distribution

The team slicer allows interactive filtering of the dashboard.

---

## Streamlit Web Application

The project includes an interactive Streamlit web application that brings the analytics, machine learning, and AI components together in a single interface.

### Streamlit Features

- Team performance analysis
- Team explorer
- Top run scorers and wicket takers
- Player analysis
- Venue analysis
- Match explorer
- AI-powered analytics insights
- ML-based match winner prediction

### Run the Application Locally

```bash
streamlit run streamlit/app.py

## 12. Machine Learning – Match Prediction

### Objective

Predict whether Team 1 will win a match.

Target:

`team1_win`

- 1 = Team 1 wins
- 0 = Team 1 does not win

Only 72 completed/decided matches were used for the match-outcome model because the No Result and Tie do not provide a binary winner target.

### Features

The final model uses 13 features:

1. team1
2. team2
3. venue
4. team1_prev_win_pct
5. team2_prev_win_pct
6. team1_recent_form
7. team2_recent_form
8. team1_avg_runs
9. team2_avg_runs
10. team1_avg_conceded
11. team2_avg_conceded
12. toss_winner_is_team1
13. toss_decision

Historical team features were calculated chronologically so that the model does not use future match results as pre-match information.

### Model Comparison

Cross-validation comparison:

| Model | Mean Accuracy | Std. Dev. |
|---|---:|---:|
| Random Forest | **57.62%** | 12.47% |
| Extra Trees | 56.50% | 11.91% |
| Logistic Regression | 53.16% | 12.12% |
| Gradient Boosting | 52.82% | 9.12% |

### Final Model

**Random Forest**

Final model file:

`models/ipl_2026_final_random_forest.pkl`

Training data:
- 72 matches
- 13 features

Example prediction:
- Team 1: RCB
- Team 2: CSK
- Predicted winner: RCB
- Team 1 probability: 60.33%
- Team 2 probability: 39.67%

### Important ML Limitation

The dataset contains only one IPL season and therefore a relatively small number of match-level observations.

The 57.62% cross-validation accuracy should therefore be treated as an experimental baseline rather than evidence of production-level prediction performance.

---

## 13. RAG / AI Analytics Layer

The project includes a local RAG-style analytics assistant.

### Retrieval

The retrieval layer searches project-generated analytical data for:
- Team performance
- Top batters
- Top bowlers
- Phase performance

### Grounded Context

Retrieved values are converted into a structured context.

Example context:

```text
Team: Royal Challengers Bengaluru
Matches: 16
Wins: 11
Losses: 5
Win Percentage: 68.75%
Runs Scored: 3057
Runs Conceded: 2933
```

### Local Answer Generation

Because no paid API key is required, the current version uses deterministic local answer generation based on retrieved project data.

This demonstrates the core RAG flow:

```text
User Question
     ↓
Retrieve Relevant Data
     ↓
Create Grounded Context
     ↓
Generate Answer
```

The retrieval layer is intentionally separated from answer generation so an LLM can be connected later without rebuilding the analytics pipeline.

---

## 14. How to Run

### Activate the environment

```powershell
& "C:\Users\rithu\venv\Scripts\Activate.ps1"
```

### Go to the project

```powershell
cd "C:\Users\rithu\Videos\AnyDesk\files\ipl dataset"
```

### Run scripts from project root

Example:

```powershell
python python\01_inspect_data.py
python python\03_find_2026.py
python python\04_create_matches.py
python python\06_create_deliveries.py
python python\08_batting_metrics.py
python python\08_bowling_metrics.py
python python\08_team_metrics.py
python python\08_phase_metrics.py
python python\09_match_analytics.py
python python\10_venue_analytics.py
python python\11_player_impact.py
python python\12_bowling_impact.py
python python\13_partnership_analytics.py
python python\14_match_turning_points.py
python python\15_team_phase_analysis.py
python python\19_compare_models.py
python python\20_train_final_model.py
python python\21_predict_match.py
python python\22_rag_retrieval.py
python python\23_rag_ai_assistant.py
```

---

## 15. Data-to-Decision Flow

The project demonstrates a complete analytics workflow:

**Raw Data**
→ collect and inspect

**Data Engineering**
→ extract and clean

**Data Quality**
→ validate and investigate anomalies

**Feature Engineering**
→ create analytical metrics

**SQL**
→ build reusable analytical views

**Excel**
→ perform business analysis

**Power BI**
→ communicate insights interactively

**Machine Learning**
→ predict match outcomes

**RAG / AI**
→ answer analytical questions using grounded project data

---

## 16. Key Project Outcomes

The completed project demonstrates practical experience with:

- Python data processing
- Pandas and NumPy
- Data cleaning and validation
- Feature engineering
- SQL analytics
- MySQL views
- Excel reporting
- Power BI dashboards
- Machine learning model comparison
- Random Forest classification
- Chronological historical feature engineering
- Retrieval-based AI analytics
- End-to-end data pipeline design

---

