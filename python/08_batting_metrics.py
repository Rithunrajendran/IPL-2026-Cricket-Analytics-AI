import pandas as pd

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/batting_metrics_2026.csv"

deliveries = pd.read_csv(DELIVERIES_PATH)

batting = deliveries.groupby("batter").agg(
    runs=("batter_runs", "sum"),
    balls_faced=("is_legal_delivery", "sum"),
    fours=("batter_runs", lambda x: (x == 4).sum()),
    sixes=("batter_runs", lambda x: (x == 6).sum()),
    dot_balls=("batter_runs", lambda x: (x == 0).sum())
).reset_index()

batting["strike_rate"] = (
    batting["runs"] / batting["balls_faced"] * 100
).round(2)

batting.to_csv(OUTPUT_PATH, index=False)

print("Batting metrics created:", len(batting))

print("\nTop 10 run scorers:")
print(
    batting.sort_values("runs", ascending=False)
    .head(10)
    .to_string(index=False)
)