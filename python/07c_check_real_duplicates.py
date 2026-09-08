import pandas as pd

DELIVERIES_PATH = "../processed/deliveries_2026.csv"

deliveries = pd.read_csv(DELIVERIES_PATH)

duplicates = deliveries[
    deliveries.duplicated(keep=False)
]

print("Number of completely duplicate rows:", len(duplicates))

print("\nNumber of duplicate rows excluding first occurrence:")
print(deliveries.duplicated().sum())

if len(duplicates) > 0:
    print("\nFirst 20 completely duplicate rows:")
    print(duplicates.head(20).to_string(index=False))
else:
    print("\nNo completely duplicate rows found.")