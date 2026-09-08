import pandas as pd

INPUT_PATH = "../processed/bowling_metrics_2026.csv"
OUTPUT_PATH = "../processed/bowling_metrics_2026.csv"

bowling = pd.read_csv(INPUT_PATH)

bowling["bowling_strike_rate"] = (
    bowling["legal_balls"] / bowling["wickets"]
).round(2)

bowling["dot_ball_percentage"] = (
    bowling["dot_balls"] /
    bowling["legal_balls"] * 100
).round(2)

bowling["bowling_average"] = (
    bowling["runs_conceded"] /
    bowling["wickets"]
).round(2)

bowling.to_csv(OUTPUT_PATH, index=False)

print("Advanced bowling metrics added.")

print("\nTop 10 wicket takers:")
print(
    bowling[
        [
            "bowler",
            "wickets",
            "runs_conceded",
            "economy",
            "bowling_strike_rate",
            "dot_ball_percentage",
            "bowling_average"
        ]
    ]
    .sort_values("wickets", ascending=False)
    .head(10)
    .to_string(index=False)
)