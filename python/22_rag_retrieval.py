import pandas as pd


# ============================================================
# 1. LOAD DATA
# ============================================================

team_data = pd.read_csv(
    "processed/team_metrics_2026.csv"
)

batting_data = pd.read_csv(
    "processed/batting_metrics_2026.csv"
)

bowling_data = pd.read_csv(
    "processed/bowling_metrics_2026.csv"
)

phase_data = pd.read_csv(
    "processed/phase_metrics_2026.csv"
)

deliveries_data = pd.read_csv(
    "processed/deliveries_2026.csv"
)

matches_data = pd.read_csv(
    "processed/matches_2026.csv"
)


# ============================================================
# 2. REMOVE EXACT DUPLICATES
# ============================================================

deliveries_data = deliveries_data.drop_duplicates()


# ============================================================
# 3. CREATE BOWLING TEAM
# ============================================================

deliveries_data = deliveries_data.merge(
    matches_data[
        [
            "match_id",
            "team1",
            "team2"
        ]
    ],
    on="match_id",
    how="left"
)


deliveries_data["bowling_team"] = deliveries_data.apply(
    lambda row:
        row["team2"]
        if row["batting_team"] == row["team1"]
        else row["team1"],
    axis=1
)


# ============================================================
# 4. HELPER FUNCTION
# ============================================================

def get_value(row, possible_columns, default="N/A"):

    for column in possible_columns:

        if column in row.index:

            value = row[column]

            if pd.notna(value):
                return value

    return default


# ============================================================
# 5. RETRIEVE TEAM INFORMATION
# ============================================================

def retrieve_team_info(team):

    result = team_data[
        team_data["team"].astype(str).str.lower()
        == team.lower()
    ]

    if result.empty:
        return None

    return result.iloc[0]


# ============================================================
# 6. RETRIEVE BATTING INFORMATION
# ============================================================

def retrieve_batting_info(team):

    team_deliveries = deliveries_data[
        deliveries_data["batting_team"].astype(str).str.lower()
        == team.lower()
    ]

    if team_deliveries.empty:
        return None

    batters = team_deliveries["batter"].dropna().unique()

    result = batting_data[
        batting_data["batter"].isin(batters)
    ].copy()

    if result.empty:
        return None

    return result.sort_values(
        "runs",
        ascending=False
    ).head(10)


# ============================================================
# 7. RETRIEVE BOWLING INFORMATION
# ============================================================

def retrieve_bowling_info(team):

    team_deliveries = deliveries_data[
        deliveries_data["bowling_team"].astype(str).str.lower()
        == team.lower()
    ]

    if team_deliveries.empty:
        return None

    bowlers = team_deliveries["bowler"].dropna().unique()

    result = bowling_data[
        bowling_data["bowler"].isin(bowlers)
    ].copy()

    if result.empty:
        return None

    return result.sort_values(
        "wickets",
        ascending=False
    ).head(10)


# ============================================================
# 8. RETRIEVE PHASE INFORMATION
# ============================================================

def retrieve_phase_info(team):

    result = phase_data[
        phase_data["batting_team"].astype(str).str.lower()
        == team.lower()
    ]

    if result.empty:
        return None

    return result.sort_values(
        "run_rate",
        ascending=False
    )


# ============================================================
# 9. SYSTEM HEADER
# ============================================================

print("\n" + "=" * 65)
print("ASK THE IPL ANALYTICS SYSTEM")
print("=" * 65)


# ============================================================
# 10. SHOW AVAILABLE TEAMS
# ============================================================

print("\nAvailable teams:")

for team in sorted(team_data["team"].dropna().unique()):

    print("-", team)


# ============================================================
# 11. USER INPUT
# ============================================================

team = input(
    "\nEnter a team name: "
).strip()


# ============================================================
# 12. RETRIEVE DATA
# ============================================================

team_info = retrieve_team_info(team)

batting_info = retrieve_batting_info(team)

bowling_info = retrieve_bowling_info(team)

phase_info = retrieve_phase_info(team)


# ============================================================
# 13. TEAM VALIDATION
# ============================================================

if team_info is None:

    print("\nTeam not found.")

    print(
        "\nPlease enter a team name from the available list."
    )

    exit()


# ============================================================
# 14. TEAM SUMMARY
# ============================================================

print("\n" + "=" * 65)
print("RETRIEVED TEAM INFORMATION")
print("=" * 65)

team_name = get_value(
    team_info,
    ["team"]
)

matches = get_value(
    team_info,
    ["matches", "matches_played"]
)

wins = get_value(
    team_info,
    ["wins"]
)

losses = get_value(
    team_info,
    ["losses"]
)

win_percentage = get_value(
    team_info,
    ["win_percentage", "win_pct"]
)

runs_scored = get_value(
    team_info,
    ["runs_scored"]
)

runs_conceded = get_value(
    team_info,
    ["runs_conceded"]
)


print("\nTeam:", team_name)

print("Matches:", matches)

print("Wins:", wins)

print("Losses:", losses)

print(
    "Win Percentage:",
    win_percentage,
    "%"
)

print(
    "Runs Scored:",
    runs_scored
)

print(
    "Runs Conceded:",
    runs_conceded
)


# ============================================================
# 15. TOP BATTERS
# ============================================================

print("\n" + "=" * 65)
print("TOP BATTERS — RETRIEVED DATA")
print("=" * 65)

if batting_info is not None:

    batting_columns = [
        "batter",
        "runs",
        "strike_rate"
    ]

    available_columns = [
        column
        for column in batting_columns
        if column in batting_info.columns
    ]

    print(
        batting_info[
            available_columns
        ].to_string(index=False)
    )

else:

    print("No batting data available.")


# ============================================================
# 16. TOP BOWLERS
# ============================================================

print("\n" + "=" * 65)
print("TOP BOWLERS — RETRIEVED DATA")
print("=" * 65)

if bowling_info is not None:

    bowling_columns = [
        "bowler",
        "wickets",
        "economy"
    ]

    available_columns = [
        column
        for column in bowling_columns
        if column in bowling_info.columns
    ]

    print(
        bowling_info[
            available_columns
        ].to_string(index=False)
    )

else:

    print("No bowling data available.")


# ============================================================
# 17. PHASE PERFORMANCE
# ============================================================

print("\n" + "=" * 65)
print("PHASE PERFORMANCE — RETRIEVED DATA")
print("=" * 65)

if phase_info is not None:

    phase_columns = [
        "phase",
        "runs",
        "run_rate",
        "wickets"
    ]

    available_columns = [
        column
        for column in phase_columns
        if column in phase_info.columns
    ]

    print(
        phase_info[
            available_columns
        ].to_string(index=False)
    )

else:

    print("No phase data available.")


# ============================================================
# 18. BUILD BATTING CONTEXT
# ============================================================

if batting_info is not None:

    batting_columns = [
        "batter",
        "runs",
        "strike_rate"
    ]

    available_columns = [
        column
        for column in batting_columns
        if column in batting_info.columns
    ]

    batting_context = batting_info[
        available_columns
    ].to_string(index=False)

else:

    batting_context = "No batting data available."


# ============================================================
# 19. BUILD BOWLING CONTEXT
# ============================================================

if bowling_info is not None:

    bowling_columns = [
        "bowler",
        "wickets",
        "economy"
    ]

    available_columns = [
        column
        for column in bowling_columns
        if column in bowling_info.columns
    ]

    bowling_context = bowling_info[
        available_columns
    ].to_string(index=False)

else:

    bowling_context = "No bowling data available."


# ============================================================
# 20. BUILD PHASE CONTEXT
# ============================================================

if phase_info is not None:

    phase_columns = [
        "phase",
        "runs",
        "run_rate",
        "wickets"
    ]

    available_columns = [
        column
        for column in phase_columns
        if column in phase_info.columns
    ]

    phase_context = phase_info[
        available_columns
    ].to_string(index=False)

else:

    phase_context = "No phase data available."


# ============================================================
# 21. CREATE GROUNDED RAG CONTEXT
# ============================================================

context = f"""

IPL 2026 ANALYTICS CONTEXT

TEAM
{team_name}

MATCHES
{matches}

WINS
{wins}

LOSSES
{losses}

WIN PERCENTAGE
{win_percentage}%

RUNS SCORED
{runs_scored}

RUNS CONCEDED
{runs_conceded}


TOP BATTERS

{batting_context}


TOP BOWLERS

{bowling_context}


PHASE PERFORMANCE

{phase_context}

"""


# ============================================================
# 22. DISPLAY GROUNDED CONTEXT
# ============================================================

print("\n" + "=" * 65)
print("GROUNDED CONTEXT FOR AI")
print("=" * 65)

print(context)


# ============================================================
# 23. COMPLETION
# ============================================================

print("=" * 65)

print(
    "RAG RETRIEVAL COMPLETED SUCCESSFULLY."
)

print("=" * 65)