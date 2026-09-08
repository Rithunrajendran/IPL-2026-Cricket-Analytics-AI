import pandas as pd


# ==========================================
# FILE PATHS
# ==========================================

BOWLING_PATH = "../processed/bowling_metrics_2026.csv"
OUTPUT_PATH = "../processed/bowling_impact_2026.csv"


# ==========================================
# LOAD DATA
# ==========================================

bowling = pd.read_csv(BOWLING_PATH)


# ==========================================
# BOWLING IMPACT METRICS
# ==========================================

bowling_impact = bowling.copy()


# ==========================================
# 3+ WICKET HAULS
# ==========================================

deliveries_path = "../processed/deliveries_2026.csv"

deliveries = pd.read_csv(deliveries_path)


# Count bowler-credited wickets
valid_wickets = [
    "caught",
    "bowled",
    "lbw",
    "caught and bowled",
    "stumped",
    "hit wicket"
]

deliveries["bowler_wicket"] = (
    deliveries["dismissal_type"]
    .isin(valid_wickets)
    .astype(int)
)


# ==========================================
# WICKETS PER MATCH
# ==========================================

bowler_match_wickets = (
    deliveries
    .groupby(["match_id", "bowler"])
    .agg(
        match_wickets=("bowler_wicket", "sum")
    )
    .reset_index()
)


# ==========================================
# WICKET HAULS
# ==========================================

wicket_hauls = (
    bowler_match_wickets
    .groupby("bowler")
    .agg(
        matches_bowled=("match_id", "count"),
        three_plus_wickets=(
            "match_wickets",
            lambda x: (x >= 3).sum()
        ),
        four_plus_wickets=(
            "match_wickets",
            lambda x: (x >= 4).sum()
        ),
        five_plus_wickets=(
            "match_wickets",
            lambda x: (x >= 5).sum()
        ),
        best_match_wickets=("match_wickets", "max")
    )
    .reset_index()
)


# ==========================================
# MERGE WITH BOWLING METRICS
# ==========================================

bowling_impact = bowling_impact.merge(
    wicket_hauls,
    on="bowler",
    how="left"
)


# ==========================================
# ROUND VALUES
# ==========================================

bowling_impact["bowling_average"] = (
    bowling_impact["runs_conceded"]
    / bowling_impact["wickets"]
).round(2)

bowling_impact["bowling_strike_rate"] = (
    bowling_impact["legal_balls"]
    / bowling_impact["wickets"]
).round(2)

bowling_impact["dot_ball_percentage"] = (
    bowling_impact["dot_balls"]
    / bowling_impact["legal_balls"]
    * 100
).round(2)


# ==========================================
# SORT BY WICKETS
# ==========================================

bowling_impact = bowling_impact.sort_values(
    "wickets",
    ascending=False
)


# ==========================================
# SAVE OUTPUT
# ==========================================

bowling_impact.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("Bowling impact analytics created successfully!")
print("Total bowlers:", len(bowling_impact))

print("\nTop 10 bowlers:")

print(
    bowling_impact[
        [
            "bowler",
            "matches_bowled",
            "wickets",
            "runs_conceded",
            "economy",
            "bowling_average",
            "bowling_strike_rate",
            "dot_ball_percentage",
            "three_plus_wickets",
            "four_plus_wickets",
            "five_plus_wickets",
            "best_match_wickets"
        ]
    ]
    .head(10)
    .to_string(index=False)
)