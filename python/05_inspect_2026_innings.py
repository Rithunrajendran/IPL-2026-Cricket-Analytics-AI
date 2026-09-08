import json
import glob
import os

DATA_PATH = "../cricsheet_json"

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

# Find the first IPL 2026 match
for file in files:

    with open(file, "r", encoding="utf-8") as f:
        match = json.load(f)

    info = match["info"]

    if str(info.get("season")) == "2026":
        break


print("Match file:")
print(os.path.basename(file))

print("\nTeams:")
print(info.get("teams"))

print("\nNumber of innings:")
print(len(match.get("innings", [])))


# Inspect first innings
innings = match["innings"][0]

print("\nFirst innings keys:")
print(innings.keys())

print("\nBatting team:")
print(innings.get("team"))

print("\nNumber of overs:")
print(len(innings.get("overs", [])))


# Inspect first over
first_over = innings["overs"][0]

print("\nFirst over:")
print(first_over)


# Inspect first delivery
first_delivery = first_over["deliveries"][0]

print("\nFirst delivery:")
print(first_delivery)