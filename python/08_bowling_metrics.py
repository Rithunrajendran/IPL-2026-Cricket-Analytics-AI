import pandas as pd

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/bowling_metrics_2026.csv"

deliveries = pd.read_csv(DELIVERIES_PATH)

# Runs actually conceded by the bowler
deliveries["bowler_runs"] = (
    deliveries["batter_runs"]
    + deliveries["wides"]
    + deliveries["noballs"]
)

# Only these dismissals are credited to the bowler
bowler_wicket_types = [
    "caught",
    "bowled",
    "lbw",
    "caught and bowled",
    "stumped",
    "hit wicket"
]

deliveries["bowler_wicket"] = deliveries["dismissal_type"].isin(
    bowler_wicket_types
).astype(int)

# Bowling metrics
bowling = deliveries.groupby("bowler").agg(
    runs_conceded=("bowler_runs", "sum"),
    legal_balls=("is_legal_delivery", "sum"),
    dot_balls=("bowler_runs", lambda x: (x == 0).sum()),
    wickets=("bowler_wicket", "sum")
).reset_index()

# Economy rate
bowling["economy"] = (
    bowling["runs_conceded"] /
    bowling["legal_balls"] * 6
).round(2)

bowling.to_csv(OUTPUT_PATH, index=False)

print("Bowling metrics created successfully!")
print("Total bowlers:", len(bowling))

print("\nTop 10 wicket-takers:")
print(
    bowling.sort_values("wickets", ascending=False)
    .head(10)
    .to_string(index=False)
)