import pandas as pd
import joblib


# ============================================================
# 1. LOAD TRAINED MODEL
# ============================================================

model_path = "models/ipl_2026_final_random_forest.pkl"

model = joblib.load(model_path)

print("=" * 60)
print("IPL 2026 MATCH PREDICTION SYSTEM")
print("=" * 60)


# ============================================================
# 2. LOAD HISTORICAL ML FEATURES
# ============================================================

data = pd.read_csv("processed/ml_features_2026.csv")

data["match_date"] = pd.to_datetime(data["match_date"])

print("\nHistorical data loaded successfully.")
print("Matches available:", len(data))


# ============================================================
# 3. GET AVAILABLE TEAMS
# ============================================================

teams = sorted(
    set(data["team1"].dropna())
    | set(data["team2"].dropna())
)

print("\nAvailable teams:")

for team in teams:
    print("-", team)


# ============================================================
# 4. USER INPUT
# ============================================================

print("\n" + "=" * 60)
print("ENTER MATCH DETAILS")
print("=" * 60)

team1 = input("\nEnter Team 1 exactly as shown above: ").strip()

team2 = input("Enter Team 2 exactly as shown above: ").strip()

venue = input("Enter venue: ").strip()

toss_winner = input(
    "\nWho won the toss? Enter Team 1 or Team 2: "
).strip()

toss_decision = input(
    "Toss decision (bat/field): "
).strip().lower()


# ============================================================
# 5. VALIDATE INPUT
# ============================================================

if team1 not in teams:
    print("\nERROR: Team 1 was not found in the historical data.")
    print("Please use the exact team name.")
    exit()

if team2 not in teams:
    print("\nERROR: Team 2 was not found in the historical data.")
    print("Please use the exact team name.")
    exit()

if team1 == team2:
    print("\nERROR: Team 1 and Team 2 cannot be the same.")
    exit()

if toss_winner not in ["Team 1", "Team 2"]:
    print("\nERROR: Toss winner must be 'Team 1' or 'Team 2'.")
    exit()

if toss_decision not in ["bat", "field"]:
    print("\nERROR: Toss decision must be 'bat' or 'field'.")
    exit()


# ============================================================
# 6. GET LATEST HISTORICAL FEATURES FOR A TEAM
# ============================================================

def get_team_features(team):

    # Matches where the team appeared as Team 1
    team1_matches = data[
        data["team1"] == team
    ].sort_values("match_date")

    # Matches where the team appeared as Team 2
    team2_matches = data[
        data["team2"] == team
    ].sort_values("match_date")

    candidates = []

    if not team1_matches.empty:

        row = team1_matches.iloc[-1]

        candidates.append({
            "date": row["match_date"],
            "prev_win_pct": row["team1_prev_win_pct"],
            "recent_form": row["team1_recent_form"],
            "avg_runs": row["team1_avg_runs"],
            "avg_conceded": row["team1_avg_conceded"]
        })

    if not team2_matches.empty:

        row = team2_matches.iloc[-1]

        candidates.append({
            "date": row["match_date"],
            "prev_win_pct": row["team2_prev_win_pct"],
            "recent_form": row["team2_recent_form"],
            "avg_runs": row["team2_avg_runs"],
            "avg_conceded": row["team2_avg_conceded"]
        })

    if not candidates:
        return {
            "prev_win_pct": 0.5,
            "recent_form": 0.5,
            "avg_runs": data["team1_avg_runs"].mean(),
            "avg_conceded": data["team1_avg_conceded"].mean()
        }

    # Use the most recent historical information
    latest = max(
        candidates,
        key=lambda x: x["date"]
    )

    return {
        "prev_win_pct": latest["prev_win_pct"],
        "recent_form": latest["recent_form"],
        "avg_runs": latest["avg_runs"],
        "avg_conceded": latest["avg_conceded"]
    }


# ============================================================
# 7. GET HISTORICAL FEATURES
# ============================================================

team1_stats = get_team_features(team1)
team2_stats = get_team_features(team2)


# ============================================================
# 8. CREATE PREDICTION DATA
# ============================================================

toss_winner_is_team1 = (
    1 if toss_winner == "Team 1" else 0
)

prediction_data = pd.DataFrame([{

    "team1": team1,

    "team2": team2,

    "venue": venue,

    "team1_prev_win_pct":
        team1_stats["prev_win_pct"],

    "team2_prev_win_pct":
        team2_stats["prev_win_pct"],

    "team1_recent_form":
        team1_stats["recent_form"],

    "team2_recent_form":
        team2_stats["recent_form"],

    "team1_avg_runs":
        team1_stats["avg_runs"],

    "team2_avg_runs":
        team2_stats["avg_runs"],

    "team1_avg_conceded":
        team1_stats["avg_conceded"],

    "team2_avg_conceded":
        team2_stats["avg_conceded"],

    "toss_winner_is_team1":
        toss_winner_is_team1,

    "toss_decision":
        toss_decision
}])


# ============================================================
# 9. DISPLAY FEATURES USED
# ============================================================

print("\n" + "=" * 60)
print("FEATURES USED FOR PREDICTION")
print("=" * 60)

print(prediction_data.to_string(index=False))


# ============================================================
# 10. MAKE PREDICTION
# ============================================================

prediction = model.predict(prediction_data)[0]

probabilities = model.predict_proba(prediction_data)[0]

team1_probability = probabilities[1]

team2_probability = probabilities[0]


# ============================================================
# 11. DETERMINE PREDICTED WINNER
# ============================================================

if prediction == 1:
    predicted_winner = team1
else:
    predicted_winner = team2


# ============================================================
# 12. DISPLAY RESULT
# ============================================================

print("\n" + "=" * 60)
print("MATCH PREDICTION RESULT")
print("=" * 60)

print("\nTeam 1:", team1)

print("Team 2:", team2)

print("\nPredicted Winner:", predicted_winner)

print(
    "\nTeam 1 Win Probability:",
    round(team1_probability * 100, 2),
    "%"
)

print(
    "Team 2 Win Probability:",
    round(team2_probability * 100, 2),
    "%"
)

print("\n" + "=" * 60)
print("Prediction completed successfully.")
print("=" * 60)