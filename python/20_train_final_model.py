import os
import pandas as pd
import joblib

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline


# ============================================================
# 1. Load ML feature dataset
# ============================================================

data = pd.read_csv("processed/ml_features_2026.csv")

print("Dataset shape:", data.shape)


# ============================================================
# 2. Keep only matches with a clear winner
# ============================================================

data = data[data["winner"].notna()].copy()

# Target:
# 1 = Team 1 won
# 0 = Team 2 won

data["team1_win"] = (
    data["winner"] == data["team1"]
).astype(int)

print("Final training dataset:", data.shape)

print("\nTarget distribution:")
print(data["team1_win"].value_counts())


# ============================================================
# 3. Select prediction features
# ============================================================

features = [
    "team1",
    "team2",
    "venue",
    "team1_prev_win_pct",
    "team2_prev_win_pct",
    "team1_recent_form",
    "team2_recent_form",
    "team1_avg_runs",
    "team2_avg_runs",
    "team1_avg_conceded",
    "team2_avg_conceded",
    "toss_winner_is_team1",
    "toss_decision"
]

X = data[features]
y = data["team1_win"]


print("\nFeatures used by final model:")
for feature in features:
    print("-", feature)


# ============================================================
# 4. Define categorical and numerical features
# ============================================================

categorical_features = [
    "team1",
    "team2",
    "venue",
    "toss_decision"
]

numerical_features = [
    "team1_prev_win_pct",
    "team2_prev_win_pct",
    "team1_recent_form",
    "team2_recent_form",
    "team1_avg_runs",
    "team2_avg_runs",
    "team1_avg_conceded",
    "team2_avg_conceded",
    "toss_winner_is_team1"
]


# ============================================================
# 5. Preprocessing
# ============================================================

preprocessor = ColumnTransformer(
    transformers=[
        (
            "categorical",
            OneHotEncoder(handle_unknown="ignore"),
            categorical_features
        ),
        (
            "numerical",
            "passthrough",
            numerical_features
        )
    ]
)


# ============================================================
# 6. Create final Random Forest model
# ============================================================

final_model = Pipeline(
    steps=[
        (
            "preprocessor",
            preprocessor
        ),
        (
            "classifier",
            RandomForestClassifier(
                n_estimators=300,
                random_state=42,
                class_weight="balanced"
            )
        )
    ]
)


# ============================================================
# 7. Train on the complete dataset
# ============================================================

print("\nTraining final Random Forest model...")

final_model.fit(X, y)

print("Training completed successfully.")


# ============================================================
# 8. Save final model
# ============================================================

os.makedirs("models", exist_ok=True)

model_path = "models/ipl_2026_final_random_forest.pkl"

joblib.dump(
    final_model,
    model_path
)


# ============================================================
# 9. Save feature list
# ============================================================

feature_info = {
    "features": features,
    "target": "team1_win",
    "model": "Random Forest",
    "training_samples": len(data)
}

joblib.dump(
    feature_info,
    "models/ipl_2026_model_features.pkl"
)


# ============================================================
# 10. Final confirmation
# ============================================================

print("\n" + "=" * 60)
print("FINAL MODEL SAVED")
print("=" * 60)

print("Model:", "Random Forest")
print("Training samples:", len(data))
print("Features:", len(features))
print("Model path:", model_path)

print("\nThe final IPL 2026 Random Forest model is ready.")