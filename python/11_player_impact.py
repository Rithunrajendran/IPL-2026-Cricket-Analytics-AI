import pandas as pd


# ==========================================
# FILE PATHS
# ==========================================

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
BATTING_PATH = "../processed/batting_metrics_2026.csv"
MILESTONES_PATH = "../processed/player_milestones_2026.csv"
BOWLING_IMPACT_PATH = "../processed/bowling_impact_2026.csv"
OUTPUT_PATH = "../processed/player_impact_2026.csv"


# ==========================================
# LOAD DATA
# ==========================================

deliveries = pd.read_csv(DELIVERIES_PATH)
batting = pd.read_csv(BATTING_PATH)
milestones = pd.read_csv(MILESTONES_PATH)
bowling_impact = pd.read_csv(BOWLING_IMPACT_PATH)


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
# MERGE BOWLING STATS
# ==========================================

bowling_cols = [
    "bowler",
    "matches_bowled",
    "legal_balls",
    "wickets",
    "runs_conceded",
    "economy",
    "bowling_average",
    "bowling_strike_rate",
    "dot_balls",
    "dot_ball_percentage",
    "three_plus_wickets",
    "four_plus_wickets",
    "five_plus_wickets",
    "best_match_wickets"
]

# Rename bowling dot_ball_percentage to avoid clash with batting one
bowling_merge = bowling_impact[bowling_cols].copy()
bowling_merge = bowling_merge.rename(
    columns={
        "dot_ball_percentage": "bowling_dot_pct",
        "dot_balls": "bowling_dot_balls"
    }
)

player_impact = player_impact.merge(
    bowling_merge,
    left_on="batter",
    right_on="bowler",
    how="left"
)

# Drop redundant bowler name column
player_impact = player_impact.drop(columns=["bowler"])


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

print("\nTop 10 players by runs (batting stats):")

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

# Bowlers in the dataset (those who also bowled)
bowler_mask = player_impact["wickets"].notna()
print(
    f"\nPlayers with bowling stats: "
    f"{bowler_mask.sum()} / {len(player_impact)}"
)

print("\nTop 10 wicket-takers (bowling stats):")

print(
    player_impact[bowler_mask][
        [
            "batter",
            "matches_bowled",
            "wickets",
            "runs_conceded",
            "economy",
            "bowling_average",
            "bowling_strike_rate",
            "bowling_dot_pct",
            "three_plus_wickets",
            "best_match_wickets"
        ]
    ]
    .sort_values("wickets", ascending=False)
    .head(10)
    .to_string(index=False)
)