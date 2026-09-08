import pandas as pd

MATCHES_PATH = "../processed/matches_2026.csv"

matches = pd.read_csv(MATCHES_PATH)

no_winner = matches[matches["winner"].isna()]

print("Matches without a winner:")
print(no_winner.to_string(index=False))

print("\nNumber of matches without a winner:")
print(len(no_winner))