import pandas as pd


# ==========================================
# FILE PATHS
# ==========================================

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
BATTING_PATH = "../processed/batting_metrics_2026.csv"
MILESTONES_PATH = "../processed/player_milestones_2026.csv"
OUTPUT_PATH = "../processed/player_impact_2026.csv"


# ==========================================
# LOAD DATA
# ==========================================

deliveries = pd.read_csv(DELIVERIES_PATH)
batting = pd.read_csv(BATTING_PATH)
milestones = pd.read_csv(MILESTONES_PATH)


# ==========================================
# PLAYER MATCH-LEVEL PERFORMANCE
# ==========================================

player_match_runs = (
    deliveries
    .groupby(["match_id", "batter"])
    .agg(
        match_runs=("batter_runs", "sum")
    )
    .reset_index()
)


# ==========================================
# PLAYER IMPACT METRICS
# ==========================================

player_impact = (
    player_match_runs
    .groupby("batter")
    .agg(
        innings=("match_id", "count"),
        average_runs=("match_runs", "mean"),
        highest_score=("match_runs", "max"),
        ducks=("match_runs", lambda x: (x == 0).sum())
    )
    .reset_index()
)


# ==========================================
# ROUND AVERAGE
# ==========================================

player_impact["average_runs"] = (
    player_impact["average_runs"].round(2)
)


# ==========================================
# MERGE BATTING METRICS
# ==========================================

player_impact = player_impact.merge(
    batting[
        [
            "batter",
            "runs",
            "balls_faced",
            "strike_rate",
            "fours",
            "sixes",
            "boundary_percentage",
            "dot_ball_percentage"
        ]
    ],
    on="batter",
    how="left"
)


# ==========================================
# MERGE MILESTONE DATA
# ==========================================

player_impact = player_impact.merge(
    milestones,
    on="batter",
    how="left"
)


# ==========================================
# CONSISTENCY METRIC
# ==========================================

player_impact["30_plus_percentage"] = (
    player_impact["scores_30_plus"]
    / player_impact["innings"]
    * 100
).round(2)


# ==========================================
# SORT BY TOTAL RUNS
# ==========================================

player_impact = player_impact.sort_values(
    "runs",
    ascending=False
)


# ==========================================
# SAVE OUTPUT
# ==========================================

player_impact.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("Player impact analytics created successfully!")
print("Total players:", len(player_impact))

print("\nTop 10 players by runs:")

print(
    player_impact[
        [
            "batter",
            "innings",
            "runs",
            "average_runs",
            "highest_score",
            "strike_rate",
            "scores_30_plus",
            "scores_50_plus",
            "scores_100_plus",
            "ducks",
            "30_plus_percentage"
        ]
    ]
    .head(10)
    .to_string(index=False)
)