import pandas as pd

DELIVERIES_PATH = "../processed/deliveries_2026.csv"

deliveries = pd.read_csv(DELIVERIES_PATH)

duplicates = deliveries[
    deliveries.duplicated(
        subset=["match_id", "innings", "over", "actual_delivery"],
        keep=False
    )
]

print("Number of duplicate rows:", len(duplicates))

print("\nFirst 30 duplicate rows:")
print(
    duplicates[
        [
            "match_id",
            "innings",
            "over",
            "actual_delivery",
            "batter",
            "bowler",
            "batter_runs",
            "extra_runs",
            "wides",
            "noballs"
        ]
    ].head(30).to_string(index=False)
)