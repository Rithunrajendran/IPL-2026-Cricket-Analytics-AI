import pandas as pd

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report


# ============================================================
# 1. Load match data
# ============================================================

matches = pd.read_csv("processed/match_analytics_2026.csv")

matches["match_date"] = pd.to_datetime(matches["match_date"])

# Keep only matches with a clear winner
ml_data = matches[matches["winner"].notna()].copy()

# Sort matches chronologically
ml_data = ml_data.sort_values("match_date").reset_index(drop=True)

# Target: 1 if Team 1 won, otherwise 0
ml_data["team1_win"] = (
    ml_data["winner"] == ml_data["team1"]
).astype(int)


# ============================================================
# 2. Create historical team features
# ============================================================

team_stats = {}

team1_prev_win_pct = []
team2_prev_win_pct = []

team1_recent_form = []
team2_recent_form = []

team1_avg_runs = []
team2_avg_runs = []

team1_avg_conceded = []
team2_avg_conceded = []


for _, row in ml_data.iterrows():

    team1 = row["team1"]
    team2 = row["team2"]

    stats1 = team_stats.get(
        team1,
        {
            "matches": 0,
            "wins": 0,
            "runs_scored": [],
            "runs_conceded": [],
            "recent_results": []
        }
    )

    stats2 = team_stats.get(
        team2,
        {
            "matches": 0,
            "wins": 0,
            "runs_scored": [],
            "runs_conceded": [],
            "recent_results": []
        }
    )

    # --------------------------------------------------------
    # Previous win percentage
    # --------------------------------------------------------

    win_pct1 = (
        stats1["wins"] / stats1["matches"]
        if stats1["matches"] > 0
        else 0.5
    )

    win_pct2 = (
        stats2["wins"] / stats2["matches"]
        if stats2["matches"] > 0
        else 0.5
    )

    team1_prev_win_pct.append(win_pct1)
    team2_prev_win_pct.append(win_pct2)

    # --------------------------------------------------------
    # Recent form
    # Last 3 matches: win = 1, loss = 0
    # --------------------------------------------------------

    recent1 = stats1["recent_results"][-3:]
    recent2 = stats2["recent_results"][-3:]

    form1 = (
        sum(recent1) / len(recent1)
        if recent1
        else 0.5
    )

    form2 = (
        sum(recent2) / len(recent2)
        if recent2
        else 0.5
    )

    team1_recent_form.append(form1)
    team2_recent_form.append(form2)

    # --------------------------------------------------------
    # Average runs scored
    # --------------------------------------------------------

    avg_runs1 = (
        sum(stats1["runs_scored"]) /
        len(stats1["runs_scored"])
        if stats1["runs_scored"]
        else 0.0
    )

    avg_runs2 = (
        sum(stats2["runs_scored"]) /
        len(stats2["runs_scored"])
        if stats2["runs_scored"]
        else 0.0
    )

    team1_avg_runs.append(avg_runs1)
    team2_avg_runs.append(avg_runs2)

    # --------------------------------------------------------
    # Average runs conceded
    # --------------------------------------------------------

    avg_conceded1 = (
        sum(stats1["runs_conceded"]) /
        len(stats1["runs_conceded"])
        if stats1["runs_conceded"]
        else 0.0
    )

    avg_conceded2 = (
        sum(stats2["runs_conceded"]) /
        len(stats2["runs_conceded"])
        if stats2["runs_conceded"]
        else 0.0
    )

    team1_avg_conceded.append(avg_conceded1)
    team2_avg_conceded.append(avg_conceded2)

    # --------------------------------------------------------
    # Update statistics AFTER current match
    # --------------------------------------------------------

    winner = row["winner"]

    team1_runs = row["first_innings_runs"] \
        if row["first_innings_team"] == team1 \
        else row["second_innings_runs"]

    team2_runs = row["first_innings_runs"] \
        if row["first_innings_team"] == team2 \
        else row["second_innings_runs"]

    # Initialize teams if needed
    for team in [team1, team2]:

        if team not in team_stats:
            team_stats[team] = {
                "matches": 0,
                "wins": 0,
                "runs_scored": [],
                "runs_conceded": [],
                "recent_results": []
            }

    # Update Team 1
    team_stats[team1]["matches"] += 1
    team_stats[team1]["runs_scored"].append(team1_runs)
    team_stats[team1]["runs_conceded"].append(team2_runs)

    if winner == team1:
        team_stats[team1]["wins"] += 1
        team_stats[team1]["recent_results"].append(1)
    else:
        team_stats[team1]["recent_results"].append(0)

    # Update Team 2
    team_stats[team2]["matches"] += 1
    team_stats[team2]["runs_scored"].append(team2_runs)
    team_stats[team2]["runs_conceded"].append(team1_runs)

    if winner == team2:
        team_stats[team2]["wins"] += 1
        team_stats[team2]["recent_results"].append(1)
    else:
        team_stats[team2]["recent_results"].append(0)


# ============================================================
# 3. Add historical features to dataset
# ============================================================

ml_data["team1_prev_win_pct"] = team1_prev_win_pct
ml_data["team2_prev_win_pct"] = team2_prev_win_pct

ml_data["team1_recent_form"] = team1_recent_form
ml_data["team2_recent_form"] = team2_recent_form

ml_data["team1_avg_runs"] = team1_avg_runs
ml_data["team2_avg_runs"] = team2_avg_runs

ml_data["team1_avg_conceded"] = team1_avg_conceded
ml_data["team2_avg_conceded"] = team2_avg_conceded


# Toss feature
ml_data["toss_winner_is_team1"] = (
    ml_data["toss_winner"] == ml_data["team1"]
).astype(int)
# Save leakage-safe engineered features
ml_data.to_csv(
    "processed/ml_features_2026.csv",
    index=False
)

print("\nML feature dataset saved successfully.")


# ============================================================
# 4. Display feature examples
# ============================================================

print("\nEnhanced historical features:")

print(
    ml_data[
        [
            "match_date",
            "team1",
            "team2",
            "team1_prev_win_pct",
            "team2_prev_win_pct",
            "team1_recent_form",
            "team2_recent_form",
            "team1_avg_runs",
            "team2_avg_runs",
            "team1_avg_conceded",
            "team2_avg_conceded",
            "team1_win"
        ]
    ].head(15)
)


# ============================================================
# 5. Select ML features
# ============================================================

features = [
    "team1",
    "team2",
    "venue",
    "toss_winner_is_team1",
    "toss_decision",
    "team1_prev_win_pct",
    "team2_prev_win_pct",
    "team1_recent_form",
    "team2_recent_form",
    "team1_avg_runs",
    "team2_avg_runs",
    "team1_avg_conceded",
    "team2_avg_conceded"
]

X = ml_data[features]
y = ml_data["team1_win"]


# ============================================================
# 6. Define preprocessing
# ============================================================

categorical_features = [
    "team1",
    "team2",
    "venue",
    "toss_decision"
]

numerical_features = [
    "toss_winner_is_team1",
    "team1_prev_win_pct",
    "team2_prev_win_pct",
    "team1_recent_form",
    "team2_recent_form",
    "team1_avg_runs",
    "team2_avg_runs",
    "team1_avg_conceded",
    "team2_avg_conceded"
]


preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# 7. Chronological train/test split
# ============================================================

split_index = int(len(ml_data) * 0.8)

X_train = X.iloc[:split_index]
X_test = X.iloc[split_index:]

y_train = y.iloc[:split_index]
y_test = y.iloc[split_index:]


print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# ============================================================
# 8. Train Random Forest
# ============================================================

model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)


model.fit(X_train, y_train)


# ============================================================
# 9. Evaluate model
# ============================================================

y_pred = model.predict(X_test)

accuracy = accuracy_score(y_test, y_pred)

print(
    "\nEnhanced Model Accuracy:",
    round(accuracy * 100, 2),
    "%"
)

print("\nClassification Report:")

print(
    classification_report(
        y_test,
        y_pred
    )
)
import os
import joblib

# Create models folder if it doesn't exist
os.makedirs("models", exist_ok=True)

# Save trained model
model_path = "models/ipl_match_prediction_model.pkl"
joblib.dump(model, model_path)

print("\nModel saved successfully:")
print(model_path)