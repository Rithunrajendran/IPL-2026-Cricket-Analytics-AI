import pandas as pd

DELIVERIES_PATH = "../processed/deliveries_2026.csv"
OUTPUT_PATH = "../processed/phase_metrics_2026.csv"

deliveries = pd.read_csv(DELIVERIES_PATH)


def get_phase(over):
    if over <= 5:
        return "Powerplay"
    elif over <= 14:
        return "Middle"
    else:
        return "Death"


deliveries["phase"] = deliveries["over"].apply(get_phase)


phase_metrics = deliveries.groupby(
    ["batting_team", "phase"]
).agg(
    runs=("total_runs", "sum"),
    legal_balls=("is_legal_delivery", "sum"),
    wickets=("is_wicket", "sum")
).reset_index()


phase_metrics["run_rate"] = (
    phase_metrics["runs"] /
    phase_metrics["legal_balls"] * 6
).round(2)


phase_metrics.to_csv(OUTPUT_PATH, index=False)

print("Phase metrics created:", len(phase_metrics))

print("\nPhase Performance:")
print(
    phase_metrics
    .sort_values(["phase", "runs"], ascending=[True, False])
    .to_string(index=False)
)