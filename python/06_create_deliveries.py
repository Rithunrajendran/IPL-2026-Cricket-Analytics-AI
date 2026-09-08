import json
import glob
import os
import pandas as pd

DATA_PATH = "../cricsheet_json"
OUTPUT_PATH = "../processed/deliveries_2026.csv"

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

deliveries = []

for file in files:

    # Open JSON file
    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    # Only IPL 2026
    if str(info.get("season")) != "2026":
        continue

    match_id = os.path.splitext(os.path.basename(file))[0]

    # Go through innings
    for innings_no, innings in enumerate(
        match.get("innings", []), start=1
    ):

        batting_team = innings.get("team")

        # Go through overs
        for over in innings.get("overs", []):

            over_number = over.get("over")

            # Go through deliveries
            for delivery in over.get("deliveries", []):

                # Players
                batter = delivery.get("batter")
                bowler = delivery.get("bowler")
                non_striker = delivery.get("non_striker")

                # Runs
                runs = delivery.get("runs", {})

                batter_runs = runs.get("batter", 0)
                extra_runs = runs.get("extras", 0)
                total_runs = runs.get("total", 0)

                # Extras
                extras = delivery.get("extras", {})

                wides = extras.get("wides", 0)
                noballs = extras.get("noballs", 0)
                byes = extras.get("byes", 0)
                legbyes = extras.get("legbyes", 0)
                penalty = extras.get("penalty", 0)

                # Legal delivery
                is_legal_delivery = (
                    1 if wides == 0 and noballs == 0 else 0
                )

                # Wickets
                wickets = delivery.get("wickets", [])

                is_wicket = 1 if wickets else 0

                if wickets:
                    dismissal_type = wickets[0].get("kind")
                    player_dismissed = wickets[0].get("player_out")
                else:
                    dismissal_type = None
                    player_dismissed = None

                # Delivery number
                actual_delivery = delivery.get("actual_delivery")

                deliveries.append({
                    "match_id": match_id,
                    "innings": innings_no,
                    "over": over_number,
                    "actual_delivery": actual_delivery,
                    "batting_team": batting_team,
                    "batter": batter,
                    "bowler": bowler,
                    "non_striker": non_striker,
                    "batter_runs": batter_runs,
                    "extra_runs": extra_runs,
                    "total_runs": total_runs,
                    "wides": wides,
                    "noballs": noballs,
                    "byes": byes,
                    "legbyes": legbyes,
                    "penalty": penalty,
                    "is_legal_delivery": is_legal_delivery,
                    "is_wicket": is_wicket,
                    "dismissal_type": dismissal_type,
                    "player_dismissed": player_dismissed
                })


# Convert to DataFrame
deliveries_df = pd.DataFrame(deliveries)

# Create processed folder if necessary
os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)

# Save CSV
deliveries_df.to_csv(OUTPUT_PATH, index=False)


print("Deliveries extracted:", len(deliveries_df))

print("\nColumns:")
print(deliveries_df.columns.tolist())

print("\nFirst 5 rows:")
print(deliveries_df.head())

print("\nWicket count:")
print(deliveries_df["is_wicket"].value_counts())

print("\nLegal delivery count:")
print(deliveries_df["is_legal_delivery"].value_counts())