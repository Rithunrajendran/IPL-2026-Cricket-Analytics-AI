import pandas as pd

MATCH_ANALYTICS_PATH = "../processed/match_analytics_2026.csv"
OUTPUT_PATH = "../processed/venue_analytics_2026.csv"

# Load match analytics
matches = pd.read_csv(MATCH_ANALYTICS_PATH)

# Venue analytics
venue_metrics = (
    matches
    .groupby(["venue", "city"])
    .agg(
        matches_played=("match_id", "nunique"),
        average_first_innings_score=("first_innings_runs", "mean"),
        average_second_innings_score=("second_innings_runs", "mean"),
        average_match_runs=("total_match_runs", "mean"),
        highest_match_score=("total_match_runs", "max"),
        chases_won=("result_type", lambda x: (x == "Chased").sum()),
        matches_defended=("result_type", lambda x: (x == "Defended").sum())
    )
    .reset_index()
)

# Chase success percentage
venue_metrics["chase_success_percentage"] = (
    venue_metrics["chases_won"]
    /
    (venue_metrics["chases_won"] + venue_metrics["matches_defended"])
    * 100
).round(2)

# Round average values
venue_metrics["average_first_innings_score"] = (
    venue_metrics["average_first_innings_score"].round(2)
)

venue_metrics["average_second_innings_score"] = (
    venue_metrics["average_second_innings_score"].round(2)
)

venue_metrics["average_match_runs"] = (
    venue_metrics["average_match_runs"].round(2)
)

# Save
venue_metrics.to_csv(OUTPUT_PATH, index=False)

# Display
print("Venue analytics created successfully!")
print("Total venues:", len(venue_metrics))

print("\nVenue Performance:")
print(
    venue_metrics
    .sort_values("average_match_runs", ascending=False)
    .to_string(index=False)
)