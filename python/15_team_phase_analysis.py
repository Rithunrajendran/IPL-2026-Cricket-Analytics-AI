import pandas as pd


# ==========================================
# FILE PATHS
# ==========================================

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/team_phase_analysis_2026.csv"


# ==========================================
# LOAD DATA
# ==========================================

deliveries = pd.read_csv(DELIVERIES_PATH)


# ==========================================
# DEFINE MATCH PHASE
# ==========================================

def get_phase(over):
    if over <= 5:
        return "Powerplay"
    elif over <= 14:
        return "Middle"
    else:
        return "Death"


deliveries["phase"] = deliveries["over"].apply(get_phase)


# ==========================================
# TEAM PHASE METRICS
# ==========================================

team_phase = (
    deliveries
    .groupby(["batting_team", "phase"])
    .agg(
        runs=("total_runs", "sum"),
        legal_balls=("is_legal_delivery", "sum"),
        wickets=("is_wicket", "sum")
    )
    .reset_index()
)


# ==========================================
# RUN RATE
# ==========================================

team_phase["run_rate"] = (
    team_phase["runs"]
    / team_phase["legal_balls"]
    * 6
).round(2)


# ==========================================
# WICKET RATE
# ==========================================

team_phase["wicket_rate"] = (
    team_phase["wickets"]
    / team_phase["legal_balls"]
    * 6
).round(2)


# ==========================================
# SORT PHASES
# ==========================================

phase_order = {
    "Powerplay": 1,
    "Middle": 2,
    "Death": 3
}

team_phase["phase_order"] = (
    team_phase["phase"].map(phase_order)
)

team_phase = team_phase.sort_values(
    ["batting_team", "phase_order"]
)


# ==========================================
# REMOVE HELPER COLUMN
# ==========================================

team_phase = team_phase.drop(
    columns=["phase_order"]
)


# ==========================================
# SAVE OUTPUT
# ==========================================

team_phase.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==========================================
# DISPLAY RESULTS
# ==========================================

print("Team phase analysis created successfully!")

print(
    "Total teams:",
    team_phase["batting_team"].nunique()
)

print(
    "Total rows:",
    len(team_phase)
)


print("\nTeam phase performance:")

print(
    team_phase.to_string(index=False)
)


# ==========================================
# BEST PHASE FOR EACH TEAM
# ==========================================

best_phase = (
    team_phase
    .sort_values("run_rate", ascending=False)
    .groupby("batting_team")
    .first()
    .reset_index()
)


print("\nBest scoring phase for each team:")

print(
    best_phase[
        [
            "batting_team",
            "phase",
            "runs",
            "run_rate"
        ]
    ]
    .sort_values("run_rate", ascending=False)
    .to_string(index=False)
)