import json
import glob
import os

DATA_PATH = "../cricsheet_json"

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

print("Total JSON files:", len(files))

# Open the first JSON file
with open(files[0], "r", encoding="utf-8") as f:
    match = json.load(f)

print("\nFile inspected:")
print(os.path.basename(files[0]))

print("\nTop-level keys:")
print(match.keys())

print("\nInfo keys:")
print(match["info"].keys())