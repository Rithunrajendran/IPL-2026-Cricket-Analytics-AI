import pandas as pd


# ==========================================
# FILE PATHS
# ==========================================

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/match_turning_points_2026.csv"


# ==========================================
# LOAD DATA
# ==========================================

deliveries = pd.read_csv(DELIVERIES_PATH)


# ==========================================
# REMOVE EXACT DUPLICATES
# ==========================================

deliveries = deliveries.drop_duplicates()


# ==========================================
# OVER-LEVEL ANALYTICS
# ==========================================

over_metrics = (
    deliveries
    .groupby(
        [
            "match_id",
            "innings",
            "batting_team",
            "over"
        ]
    )
    .agg(
        over_runs=("total_runs", "sum"),
        legal_balls=("is_legal_delivery", "sum"),
        wickets=("is_wicket", "sum")
    )
    .reset_index()
)


# ==========================================
# RUN RATE
# ==========================================

over_metrics["over_run_rate"] = (
    over_metrics["over_runs"]
    / over_metrics["legal_balls"]
    * 6
).round(2)


# ==========================================
# WICKET OVER FLAG
# ==========================================

over_metrics["wicket_over"] = (
    over_metrics["wickets"] > 0
).astype(int)


# ==========================================
# HIGH-SCORING OVER FLAG
# ==========================================

over_metrics["high_scoring_over"] = (
    over_metrics["over_runs"] >= 15
).astype(int)


# ==========================================
# MOMENTUM CATEGORY
# ==========================================

def classify_momentum(runs):
    if runs >= 15:
        return "Very High"
    elif runs >= 10:
        return "High"
    elif runs >= 6:
        return "Medium"
    else:
        return "Low"


over_metrics["momentum"] = (
    over_metrics["over_runs"]
    .apply(classify_momentum)
)


# ==========================================
# SORT DATA
# ==========================================

over_metrics = over_metrics.sort_values(
    ["match_id", "innings", "over"]
)


# ==========================================
# SAVE OUTPUT
# ==========================================

over_metrics.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("Match turning-point analytics created successfully!")

print(
    "Total over records:",
    len(over_metrics)
)

print(
    "High-scoring overs:",
    over_metrics["high_scoring_over"].sum()
)

print(
    "Overs containing wickets:",
    over_metrics["wicket_over"].sum()
)


# ==========================================
# TOP SCORING OVERS
# ==========================================

print("\nTop 10 highest-scoring overs:")

print(
    over_metrics[
        [
            "match_id",
            "innings",
            "batting_team",
            "over",
            "over_runs",
            "wickets",
            "over_run_rate",
            "momentum"
        ]
    ]
    .sort_values("over_runs", ascending=False)
    .head(10)
    .to_string(index=False)
)


# ==========================================
# TOP WICKET OVERS
# ==========================================

print("\nOvers with most wickets:")

print(
    over_metrics[
        [
            "match_id",
            "innings",
            "batting_team",
            "over",
            "over_runs",
            "wickets",
            "momentum"
        ]
    ]
    .sort_values(
        ["wickets", "over_runs"],
        ascending=[False, False]
    )
    .head(10)
    .to_string(index=False)
)