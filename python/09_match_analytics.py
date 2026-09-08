import pandas as pd

# ==============================
# FILE PATHS
# ==============================

MATCHES_PATH = "../processed/matches_2026.csv"
DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/match_analytics_2026.csv"


# ==============================
# LOAD DATA
# ==============================

matches = pd.read_csv(MATCHES_PATH)
deliveries = pd.read_csv(DELIVERIES_PATH)


# ==============================
# CALCULATE INNINGS SCORES
# ==============================

innings_scores = (
    deliveries
    .groupby(["match_id", "innings", "batting_team"])
    .agg(
        runs=("total_runs", "sum"),
        wickets=("is_wicket", "sum"),
        legal_balls=("is_legal_delivery", "sum")
    )
    .reset_index()
)


# ==============================
# CREATE MATCH-LEVEL DATA
# ==============================

match_records = []

for match_id, group in innings_scores.groupby("match_id"):

    match_info = matches[matches["match_id"] == match_id].iloc[0]

    innings = group.sort_values("innings")

    # First innings
    first_innings = innings.iloc[0]

    # Second innings
    second_innings = innings.iloc[1] if len(innings) > 1 else None

    first_team = first_innings["batting_team"]
    first_runs = first_innings["runs"]

    if second_innings is not None:
        second_team = second_innings["batting_team"]
        second_runs = second_innings["runs"]
    else:
        second_team = None
        second_runs = None

    winner = match_info["winner"]

    # ==============================
    # RESULT TYPE
    # ==============================

    if pd.notna(winner):

        if winner == first_team:
            result_type = "Defended"
        elif second_innings is not None and winner == second_team:
            result_type = "Chased"
        else:
            result_type = "Other"

    else:

        if (
            second_innings is not None
            and first_runs == second_runs
        ):
            result_type = "Tie"
        else:
            result_type = "No Result"

    # ==============================
    # RUN MARGIN
    # ==============================

    run_margin = None

    if (
        pd.notna(winner)
        and second_innings is not None
        and winner == first_team
    ):
        run_margin = first_runs - second_runs

    # ==============================
    # WICKET MARGIN
    # ==============================

    wickets_margin = None

    if (
        pd.notna(winner)
        and second_innings is not None
        and winner == second_team
    ):
        wickets_lost = second_innings["wickets"]

        wickets_margin = 10 - wickets_lost

    # ==============================
    # APPEND RECORD
    # ==============================

    match_records.append({
        "match_id": match_id,
        "match_date": match_info["match_date"],
        "venue": match_info["venue"],
        "city": match_info["city"],
        "team1": match_info["team1"],
        "team2": match_info["team2"],
        "toss_winner": match_info["toss_winner"],
        "toss_decision": match_info["toss_decision"],
        "first_innings_team": first_team,
        "first_innings_runs": first_runs,
        "second_innings_team": second_team,
        "second_innings_runs": second_runs,
        "winner": winner,
        "result_type": result_type,
        "run_margin": run_margin,
        "wickets_margin": wickets_margin,
        "total_match_runs": (
            first_runs + second_runs
            if pd.notna(second_runs)
            else first_runs
        )
    })


# ==============================
# CREATE DATAFRAME
# ==============================

match_analytics = pd.DataFrame(match_records)


# ==============================
# SAVE OUTPUT
# ==============================

match_analytics.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==============================
# VALIDATION / PREVIEW
# ==============================

print("Match analytics created successfully!")
print("Total matches:", len(match_analytics))

print("\nColumns:")
print(match_analytics.columns.tolist())

print("\nResult types:")
print(match_analytics["result_type"].value_counts())

print("\nTop 10 highest-scoring matches:")

print(
    match_analytics[
        [
            "match_id",
            "match_date",
            "team1",
            "team2",
            "first_innings_runs",
            "second_innings_runs",
            "total_match_runs",
            "winner",
            "result_type"
        ]
    ]
    .sort_values("total_match_runs", ascending=False)
    .head(10)
    .to_string(index=False)
)