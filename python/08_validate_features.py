import pandas as pd

BATTING_PATH = "../processed/batting_metrics_2026.csv"
BOWLING_PATH = "../processed/bowling_metrics_2026.csv"
PHASE_PATH = "../processed/phase_metrics_2026.csv"
TEAM_PATH = "../processed/team_metrics_2026.csv"

batting = pd.read_csv(BATTING_PATH)
bowling = pd.read_csv(BOWLING_PATH)
phase = pd.read_csv(PHASE_PATH)
teams = pd.read_csv(TEAM_PATH)

print("========== BATTING ==========")

print("Players:", len(batting))
print("Negative runs:", (batting["runs"] < 0).sum())
print("Strike rate missing:", batting["strike_rate"].isna().sum())

print("\nTop 5 run scorers:")
print(
    batting.sort_values("runs", ascending=False)
    .head(5)
    .to_string(index=False)
)


print("\n========== BOWLING ==========")

print("Bowlers:", len(bowling))
print("Negative runs conceded:", (bowling["runs_conceded"] < 0).sum())
print("Economy missing:", bowling["economy"].isna().sum())

print("\nTop 5 wicket takers:")
print(
    bowling.sort_values("wickets", ascending=False)
    .head(5)
    .to_string(index=False)
)


print("\n========== TEAM ==========")

print("Teams:", len(teams))

print(
    teams.sort_values(
        "win_percentage",
        ascending=False
    ).to_string(index=False)
)


print("\n========== PHASE ==========")

print("Phase categories:")
print(phase["phase"].unique())

print("\nRows:", len(phase))