import pandas as pd


# ==========================================
# FILE PATHS
# ==========================================

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/partnership_analytics_2026.csv"


# ==========================================
# LOAD DATA
# ==========================================

deliveries = pd.read_csv(DELIVERIES_PATH)


# ==========================================
# REMOVE EXACT SOURCE DUPLICATES
# ==========================================

deliveries = deliveries.drop_duplicates()


# ==========================================
# SORT DELIVERIES
# ==========================================

deliveries = deliveries.sort_values(
    ["match_id", "innings", "over", "actual_delivery"]
)


# ==========================================
# CREATE PARTNERSHIPS
# ==========================================

partnerships = []

current_match = None
current_innings = None
current_batting_team = None

current_batter1 = None
current_batter2 = None
partnership_runs = 0
legal_balls = 0


def save_partnership():
    if current_batter1 is not None and partnership_runs > 0:
        batter1, batter2 = sorted(
            [current_batter1, current_batter2]
        )

        partnerships.append(
            {
                "match_id": current_match,
                "innings": current_innings,
                "batting_team": current_batting_team,
                "batter1": batter1,
                "batter2": batter2,
                "partnership_runs": partnership_runs,
                "legal_balls": legal_balls
            }
        )


for _, row in deliveries.iterrows():

    match_id = row["match_id"]
    innings = row["innings"]
    batting_team = row["batting_team"]

    batter = row["batter"]
    non_striker = row["non_striker"]

    # New innings
    if (
        match_id != current_match
        or innings != current_innings
    ):

        save_partnership()

        current_match = match_id
        current_innings = innings
        current_batting_team = batting_team

        current_batter1 = batter
        current_batter2 = non_striker

        partnership_runs = 0
        legal_balls = 0

    # Detect change in batting pair
    if (
        {current_batter1, current_batter2}
        != {batter, non_striker}
    ):

        save_partnership()

        current_batter1 = batter
        current_batter2 = non_striker

        partnership_runs = 0
        legal_balls = 0

    # Add runs to partnership
    partnership_runs += row["total_runs"]

    # Count legal deliveries
    legal_balls += row["is_legal_delivery"]

    # Wicket ends the current partnership
    if row["is_wicket"] == 1:

        save_partnership()

        current_batter1 = None
        current_batter2 = None

        partnership_runs = 0
        legal_balls = 0


# Save final partnership
save_partnership()


# ==========================================
# CREATE DATAFRAME
# ==========================================

partnerships_df = pd.DataFrame(partnerships)


# ==========================================
# PARTNERSHIP SUMMARY
# ==========================================

partnership_summary = (
    partnerships_df
    .groupby(["batting_team", "batter1", "batter2"])
    .agg(
        partnerships=("partnership_runs", "count"),
        total_partnership_runs=("partnership_runs", "sum"),
        average_partnership_runs=("partnership_runs", "mean"),
        highest_partnership=("partnership_runs", "max")
    )
    .reset_index()
)


# ==========================================
# ROUND VALUES
# ==========================================

partnership_summary["average_partnership_runs"] = (
    partnership_summary["average_partnership_runs"]
    .round(2)
)


# ==========================================
# SORT BY BEST PARTNERSHIP
# ==========================================

partnership_summary = partnership_summary.sort_values(
    "highest_partnership",
    ascending=False
)


# ==========================================
# SAVE OUTPUT
# ==========================================

partnership_summary.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("Partnership analytics created successfully!")

print(
    "Total partnership combinations:",
    len(partnership_summary)
)

print(
    "Total partnership innings:",
    len(partnerships_df)
)


print("\nTop 10 partnerships:")

print(
    partnership_summary[
        [
            "batting_team",
            "batter1",
            "batter2",
            "partnerships",
            "total_partnership_runs",
            "average_partnership_runs",
            "highest_partnership"
        ]
    ]
    .head(10)
    .to_string(index=False)
)