import pandas as pd

MATCHES_PATH = "../processed/matches_2026.csv"
DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/team_metrics_2026.csv"

matches = pd.read_csv(MATCHES_PATH)
deliveries = pd.read_csv(DELIVERIES_PATH)

# Create a match-to-team mapping
team_mapping = matches[
    ["match_id", "team1", "team2"]
]

deliveries = deliveries.merge(
    team_mapping,
    on="match_id",
    how="left"
)

# Determine the bowling team
deliveries["bowling_team"] = deliveries.apply(
    lambda row: (
        row["team2"]
        if row["batting_team"] == row["team1"]
        else row["team1"]
    ),
    axis=1
)

teams = pd.unique(
    matches[["team1", "team2"]].values.ravel()
)

team_metrics = []

for team in teams:

    team_matches = matches[
        (matches["team1"] == team) |
        (matches["team2"] == team)
    ]

    matches_played = len(team_matches)

    wins = (team_matches["winner"] == team).sum()

    losses = (
        (team_matches["winner"].notna()) &
        (team_matches["winner"] != team)
    ).sum()

    runs_scored = deliveries[
        deliveries["batting_team"] == team
    ]["total_runs"].sum()

    runs_conceded = deliveries[
        deliveries["bowling_team"] == team
    ]["total_runs"].sum()

    win_percentage = (
        wins / matches_played * 100
        if matches_played > 0 else 0
    )

    team_metrics.append({
        "team": team,
        "matches_played": matches_played,
        "wins": wins,
        "losses": losses,
        "win_percentage": round(win_percentage, 2),
        "runs_scored": runs_scored,
        "runs_conceded": runs_conceded
    })

team_df = pd.DataFrame(team_metrics)

team_df.to_csv(OUTPUT_PATH, index=False)

print("Team metrics created:", len(team_df))

print("\nTeam Performance:")
print(
    team_df.sort_values(
        "win_percentage",
        ascending=False
    ).to_string(index=False)
)