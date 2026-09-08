import os
import glob

DATA_PATH = "../cricsheet_json"

files = glob.glob(os.path.join(DATA_PATH, "*.json"))

print("Total JSON files:", len(files))

print("\nFirst 10 files:")
for file in files[:10]:
    print(os.path.basename(file))