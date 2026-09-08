import json
import glob
import os
import pandas as pd

DATA_PATH = "../cricsheet_json"
OUTPUT_PATH = "../processed/matches_2026.csv"

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

matches = []

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    # Keep only IPL 2026
    if str(info.get("season")) != "2026":
        continue

    teams = info.get("teams", [])
    toss = info.get("toss", {})
    outcome = info.get("outcome", {})

    match_record = {
        "match_id": os.path.splitext(os.path.basename(file))[0],

        "season": info.get("season"),

        "match_date": info.get("dates", [None])[0],

        "venue": info.get("venue"),

        "city": info.get("city"),

        "team1": teams[0] if len(teams) > 0 else None,

        "team2": teams[1] if len(teams) > 1 else None,

        "toss_winner": toss.get("winner"),

        "toss_decision": toss.get("decision"),

        "winner": outcome.get("winner"),

        "result_type": outcome.get("result"),

        "player_of_match": (
            info.get("player_of_match", [None])[0]
            if info.get("player_of_match")
            else None
        )
    }

    matches.append(match_record)


# Convert to DataFrame
matches_df = pd.DataFrame(matches)

# Make sure processed folder exists
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save CSV
matches_df.to_csv(OUTPUT_PATH, index=False)

print("Matches extracted:", len(matches_df))

print("\nColumns:")
print(matches_df.columns.tolist())

print("\nFirst 5 rows:")
print(matches_df.head())