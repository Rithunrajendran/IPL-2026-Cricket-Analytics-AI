import pandas as pd

INPUT_PATH = "../processed/batting_metrics_2026.csv"
OUTPUT_PATH = "../processed/batting_metrics_2026.csv"

batting = pd.read_csv(INPUT_PATH)

batting["boundary_runs"] = (
    batting["fours"] * 4 +
    batting["sixes"] * 6
)

batting["boundary_percentage"] = (
    batting["boundary_runs"] /
    batting["runs"] * 100
).round(2)

batting["dot_ball_percentage"] = (
    batting["dot_balls"] /
    batting["balls_faced"] * 100
).round(2)

batting.to_csv(OUTPUT_PATH, index=False)

print("Advanced batting metrics added.")

print("\nTop 10 players by boundary percentage:")
print(
    batting[
        [
            "batter",
            "runs",
            "fours",
            "sixes",
            "boundary_percentage",
            "dot_ball_percentage"
        ]
    ]
    .sort_values("boundary_percentage", ascending=False)
    .head(10)
    .to_string(index=False)
)