import json
import glob
import os

DATA_PATH = "../cricsheet_json"

total_duplicate_groups = 0
total_duplicate_records = 0

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    if str(info.get("season")) != "2026":
        continue

    for innings in match.get("innings", []):

        for over in innings.get("overs", []):

            deliveries = over.get("deliveries", [])

            seen = set()

            for delivery in deliveries:

                delivery_key = str(delivery)

                if delivery_key in seen:
                    total_duplicate_records += 1
                else:
                    seen.add(delivery_key)

            unique_count = len(set(str(d) for d in deliveries))

            if unique_count < len(deliveries):
                total_duplicate_groups += 1

print("Duplicate delivery groups:", total_duplicate_groups)
print("Repeated delivery records:", total_duplicate_records)