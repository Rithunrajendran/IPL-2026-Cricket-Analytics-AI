import pandas as pd

from sklearn.model_selection import RepeatedStratifiedKFold, cross_val_score
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline

from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import (
    RandomForestClassifier,
    GradientBoostingClassifier,
    ExtraTreesClassifier
)


# ============================================================
# 1. Load engineered ML dataset
# ============================================================

data = pd.read_csv("processed/ml_features_2026.csv")

print("Dataset shape:", data.shape)


# ============================================================
# 2. Features and target
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
    "team1_avg_runs",
    "team2_avg_runs",
    "team1_avg_conceded",
    "team2_avg_conceded",
    "toss_winner_is_team1"
]

features = categorical_features + numerical_features

X = data[features]
y = data["team1_win"]


print("\nFeatures used:")
print(features)

print("\nTarget distribution:")
print(y.value_counts())


# ============================================================
# 3. Preprocessing
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
# 4. Define models
# ============================================================

models = {

    "Logistic Regression": LogisticRegression(
        max_iter=1000,
        class_weight="balanced"
    ),

    "Random Forest": RandomForestClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced"
    ),

    "Gradient Boosting": GradientBoostingClassifier(
        n_estimators=100,
        random_state=42
    ),

    "Extra Trees": ExtraTreesClassifier(
        n_estimators=300,
        random_state=42,
        class_weight="balanced"
    )
}


# ============================================================
# 5. Repeated Stratified Cross-Validation
# ============================================================

cv = RepeatedStratifiedKFold(
    n_splits=5,
    n_repeats=5,
    random_state=42
)


# ============================================================
# 6. Compare models
# ============================================================

results = []

print("\n" + "=" * 65)
print("REPEATED CROSS-VALIDATION MODEL COMPARISON")
print("=" * 65)

for name, classifier in models.items():

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("classifier", classifier)
        ]
    )

    scores = cross_val_score(
        pipeline,
        X,
        y,
        cv=cv,
        scoring="accuracy"
    )

    mean_accuracy = scores.mean() * 100
    std_accuracy = scores.std() * 100

    results.append({
        "model": name,
        "mean_accuracy": round(mean_accuracy, 2),
        "std_accuracy": round(std_accuracy, 2)
    })

    print(f"\n{name}")
    print("-" * 45)
    print("Mean Accuracy:", round(mean_accuracy, 2), "%")
    print("Standard Deviation:", round(std_accuracy, 2), "%")


# ============================================================
# 7. Final comparison table
# ============================================================

results_df = pd.DataFrame(results)

results_df = results_df.sort_values(
    "mean_accuracy",
    ascending=False
)

print("\n" + "=" * 65)
print("FINAL MODEL COMPARISON")
print("=" * 65)

print(results_df.to_string(index=False))


# ============================================================
# 8. Save comparison results
# ============================================================

results_df.to_csv(
    "processed/model_comparison_2026.csv",
    index=False
)

print(
    "\nComparison results saved to:"
    " processed/model_comparison_2026.csv"
)


# ============================================================
# 9. Select best model
# ============================================================

best_model = results_df.iloc[0]

print("\n" + "=" * 65)
print("RECOMMENDED FINAL MODEL")
print("=" * 65)

print("Model:", best_model["model"])
print("Mean Accuracy:", best_model["mean_accuracy"], "%")
print("Standard Deviation:", best_model["std_accuracy"], "%")