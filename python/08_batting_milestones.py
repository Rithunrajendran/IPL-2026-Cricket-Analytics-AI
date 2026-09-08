import pandas as pd

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/player_milestones_2026.csv"

deliveries = pd.read_csv(DELIVERIES_PATH)

player_match_runs = (
    deliveries
    .groupby(["match_id", "batter"])["batter_runs"]
    .sum()
    .reset_index()
)

milestones = player_match_runs.groupby("batter").agg(
    scores_30_plus=("batter_runs", lambda x: (x >= 30).sum()),
    scores_50_plus=("batter_runs", lambda x: (x >= 50).sum()),
    scores_100_plus=("batter_runs", lambda x: (x >= 100).sum())
).reset_index()

milestones.to_csv(OUTPUT_PATH, index=False)

print("Player milestone metrics created:", len(milestones))

print("\nTop players by 50+ scores:")
print(
    milestones
    .sort_values("scores_50_plus", ascending=False)
    .head(10)
    .to_string(index=False)
)