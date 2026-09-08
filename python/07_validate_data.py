import pandas as pd

MATCHES_PATH = "../processed/matches_2026.csv"
DELIVERIES_PATH = "../processed/deliveries_2026.csv"

matches = pd.read_csv(MATCHES_PATH)
deliveries = pd.read_csv(DELIVERIES_PATH)

print("========== MATCH DATA ==========")

print("\nNumber of matches:")
print(len(matches))

print("\nMissing values:")
print(matches.isnull().sum())

print("\nDuplicate match IDs:")
print(matches["match_id"].duplicated().sum())

print("\nTeams:")
teams = set(matches["team1"].dropna()) | set(matches["team2"].dropna())
print(sorted(teams))


print("\n========== DELIVERY DATA ==========")

print("\nNumber of deliveries:")
print(len(deliveries))

print("\nMissing values:")
print(deliveries.isnull().sum())

print("\nDuplicate delivery records:")
print(
    deliveries.duplicated(
        subset=["match_id", "innings", "over", "actual_delivery"]
    ).sum()
)


print("\n========== RUN VALIDATION ==========")

print("\nBatter runs:")
print(deliveries["batter_runs"].describe())

print("\nExtra runs:")
print(deliveries["extra_runs"].describe())

print("\nTotal runs:")
print(deliveries["total_runs"].describe())


print("\n========== WICKET VALIDATION ==========")

print("\nWicket count:")
print(deliveries["is_wicket"].value_counts())

print("\nDismissal types:")
print(deliveries["dismissal_type"].value_counts(dropna=False))


print("\n========== LEGAL DELIVERY ==========")

print(deliveries["is_legal_delivery"].value_counts())

print("\nWides:")
print(deliveries["wides"].sum())

print("\nNo-balls:")
print(deliveries["noballs"].sum())          