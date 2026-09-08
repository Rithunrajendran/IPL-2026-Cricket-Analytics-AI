import pandas as pd

# Load IPL 2026 match analytics data
matches = pd.read_csv("processed/match_analytics_2026.csv")

print("Dataset shape:", matches.shape)
print("\nColumns:")
print(matches.columns.tolist())

print("\nFirst 5 rows:")
print(matches.head())
# Keep only completed matches with a clear winner
ml_data = matches[
    matches["winner"].notna()
].copy()

# Target: 1 if Team 1 won, otherwise 0
ml_data["team1_win"] = (
    ml_data["winner"] == ml_data["team1"]
).astype(int)

print("\nML dataset shape:", ml_data.shape)

print("\nTarget distribution:")
print(ml_data["team1_win"].value_counts())

print("\nSample target values:")
print(
    ml_data[
        ["team1", "team2", "winner", "team1_win"]
    ].head(10)
)
# Create pre-match features
ml_data["toss_winner_is_team1"] = (
    ml_data["toss_winner"] == ml_data["team1"]
).astype(int)

# Select only information available before the match
features = [
    "team1",
    "team2",
    "venue",
    "toss_winner_is_team1",
    "toss_decision"
]

X = ml_data[features]
y = ml_data["team1_win"]

print("\nFeatures used for prediction:")
print(features)

print("\nFeature data:")
print(X.head())

print("\nTarget:")
print(y.head())
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder

# Categorical and numerical features
categorical_features = [
    "team1",
    "team2",
    "venue",
    "toss_decision"
]

numerical_features = [
    "toss_winner_is_team1"
]

# Preprocessing
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

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))

print("\nPreprocessing setup completed.")
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, classification_report

# Create the ML pipeline
model = Pipeline(
    steps=[
        ("preprocessor", preprocessor),
        ("classifier", RandomForestClassifier(
            n_estimators=200,
            random_state=42,
            class_weight="balanced"
        ))
    ]
)

# Train the model
model.fit(X_train, y_train)

# Make predictions
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)

print("\nModel Accuracy:", round(accuracy * 100, 2), "%")

print("\nClassification Report:")
print(classification_report(y_test, y_pred))