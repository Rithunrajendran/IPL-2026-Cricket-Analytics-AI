import json
import glob
import os

DATA_PATH = "../cricsheet_json"

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

count = 0

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    season = info.get("season")

    if str(season) == "2026":

        count += 1

        print(
            os.path.basename(file),
            "|",
            info.get("dates"),
            "|",
            info.get("teams")
        )

print("\nTotal IPL 2026 matches:", count)