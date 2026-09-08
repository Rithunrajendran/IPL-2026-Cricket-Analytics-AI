import pandas as pd
import os


# ============================================================
# IPL 2026 LOCAL RAG ANALYTICS ASSISTANT
# ============================================================
#
# This version does NOT require an API key.
#
# Flow:
# User Question
#       ↓
# Retrieve relevant IPL data
#       ↓
# Build grounded context
#       ↓
# Generate a local analytical answer
#
# ============================================================


# ------------------------------------------------------------
# 1. File paths
# ------------------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROCESSED_DIR = os.path.join(BASE_DIR, "processed")


# ------------------------------------------------------------
# 2. Load IPL datasets
# ------------------------------------------------------------

team_file = os.path.join(
    PROCESSED_DIR,
    "team_metrics_2026.csv"
)

batting_file = os.path.join(
    PROCESSED_DIR,
    "batting_metrics_2026.csv"
)

bowling_file = os.path.join(
    PROCESSED_DIR,
    "bowling_metrics_2026.csv"
)

phase_file = os.path.join(
    PROCESSED_DIR,
    "phase_metrics_2026.csv"
)


# ------------------------------------------------------------
# 3. Load data safely
# ------------------------------------------------------------

def load_data():

    data = {}

    # Team data
    try:
        data["team"] = pd.read_csv(team_file)
    except FileNotFoundError:
        data["team"] = None

    # Batting data
    try:
        data["batting"] = pd.read_csv(batting_file)
    except FileNotFoundError:
        data["batting"] = None

    # Bowling data
    try:
        data["bowling"] = pd.read_csv(bowling_file)
    except FileNotFoundError:
        data["bowling"] = None

    # Phase data
    try:
        data["phase"] = pd.read_csv(phase_file)
    except FileNotFoundError:
        data["phase"] = None

    return data


# ------------------------------------------------------------
# 4. Find a team
# ------------------------------------------------------------

def find_team(team_name, team_data):

    if team_data is None:
        return None

    team_name = team_name.lower().strip()

    # Try exact/partial match against team column
    possible_columns = ["team", "batting_team"]

    for column in possible_columns:

        if column not in team_data.columns:
            continue

        result = team_data[
            team_data[column]
            .astype(str)
            .str.lower()
            .str.contains(team_name, regex=False)
        ]

        if not result.empty:
            return result.iloc[0]

    return None


# ------------------------------------------------------------
# 5. Retrieve team information
# ------------------------------------------------------------

def retrieve_team_info(team_name, data):

    team_data = data["team"]

    result = find_team(team_name, team_data)

    if result is None:
        return None

    return result


# ------------------------------------------------------------
# 6. Retrieve top batters for a team
# ------------------------------------------------------------

def retrieve_batting_info(team_name, data):

    batting_data = data["batting"]

    if batting_data is None:
        return None

    # The batting dataset contains player-level information.
    # Try to identify a team column.
    team_column = None

    for column in ["team", "batting_team"]:
        if column in batting_data.columns:
            team_column = column
            break

    if team_column is None:
        return None

    result = batting_data[
        batting_data[team_column]
        .astype(str)
        .str.lower()
        .str.contains(team_name.lower(), regex=False)
    ]

    if result.empty:
        return None

    if "runs" in result.columns:
        result = result.sort_values(
            "runs",
            ascending=False
        )

    return result.head(5)


# ------------------------------------------------------------
# 7. Retrieve top bowlers for a team
# ------------------------------------------------------------

def retrieve_bowling_info(team_name, data):

    bowling_data = data["bowling"]

    if bowling_data is None:
        return None

    team_column = None

    for column in ["team", "bowling_team"]:
        if column in bowling_data.columns:
            team_column = column
            break

    if team_column is None:
        return None

    result = bowling_data[
        bowling_data[team_column]
        .astype(str)
        .str.lower()
        .str.contains(team_name.lower(), regex=False)
    ]

    if result.empty:
        return None

    if "wickets" in result.columns:
        result = result.sort_values(
            "wickets",
            ascending=False
        )

    return result.head(5)


# ------------------------------------------------------------
# 8. Retrieve phase performance
# ------------------------------------------------------------

def retrieve_phase_info(team_name, data):

    phase_data = data["phase"]

    if phase_data is None:
        return None

    team_column = None

    for column in ["team", "batting_team"]:
        if column in phase_data.columns:
            team_column = column
            break

    if team_column is None:
        return None

    result = phase_data[
        phase_data[team_column]
        .astype(str)
        .str.lower()
        .str.contains(team_name.lower(), regex=False)
    ]

    return result


# ------------------------------------------------------------
# 9. Create grounded context
# ------------------------------------------------------------

def create_context(team_name, data):

    team_info = retrieve_team_info(
        team_name,
        data
    )

    batting_info = retrieve_batting_info(
        team_name,
        data
    )

    bowling_info = retrieve_bowling_info(
        team_name,
        data
    )

    phase_info = retrieve_phase_info(
        team_name,
        data
    )

    context = []

    context.append(
        "IPL 2026 ANALYTICS CONTEXT"
    )

    context.append(
        f"\nTEAM: {team_name}"
    )

    # --------------------------------------------------------
    # Team information
    # --------------------------------------------------------

    if team_info is not None:

        context.append("\nTEAM PERFORMANCE")

        for column, value in team_info.items():

            context.append(
                f"{column}: {value}"
            )

    # --------------------------------------------------------
    # Batting information
    # --------------------------------------------------------

    if batting_info is not None:

        context.append(
            "\nTOP BATTERS"
        )

        for _, row in batting_info.iterrows():

            player = row.get(
                "batter",
                row.get(
                    "player",
                    "Unknown"
                )
            )

            runs = row.get(
                "runs",
                "N/A"
            )

            strike_rate = row.get(
                "strike_rate",
                "N/A"
            )

            context.append(
                f"{player}: {runs} runs, "
                f"strike rate {strike_rate}"
            )

    # --------------------------------------------------------
    # Bowling information
    # --------------------------------------------------------

    if bowling_info is not None:

        context.append(
            "\nTOP BOWLERS"
        )

        for _, row in bowling_info.iterrows():

            player = row.get(
                "bowler",
                row.get(
                    "player",
                    "Unknown"
                )
            )

            wickets = row.get(
                "wickets",
                "N/A"
            )

            economy = row.get(
                "economy",
                "N/A"
            )

            context.append(
                f"{player}: {wickets} wickets, "
                f"economy {economy}"
            )

    # --------------------------------------------------------
    # Phase information
    # --------------------------------------------------------

    if phase_info is not None and not phase_info.empty:

        context.append(
            "\nPHASE PERFORMANCE"
        )

        for _, row in phase_info.iterrows():

            phase = row.get(
                "phase",
                "Unknown"
            )

            runs = row.get(
                "runs",
                "N/A"
            )

            run_rate = row.get(
                "run_rate",
                "N/A"
            )

            wickets = row.get(
                "wickets",
                "N/A"
            )

            context.append(
                f"{phase}: {runs} runs, "
                f"run rate {run_rate}, "
                f"{wickets} wickets"
            )

    return "\n".join(context)


# ------------------------------------------------------------
# 10. Local answer generation
# ------------------------------------------------------------

def generate_local_answer(
    question,
    team_name,
    data
):

    team_info = retrieve_team_info(
        team_name,
        data
    )

    batting_info = retrieve_batting_info(
        team_name,
        data
    )

    bowling_info = retrieve_bowling_info(
        team_name,
        data
    )

    phase_info = retrieve_phase_info(
        team_name,
        data
    )

    question_lower = question.lower()

    # --------------------------------------------------------
    # Team performance question
    # --------------------------------------------------------

    if (
        "performance" in question_lower
        or "perform" in question_lower
        or "strong" in question_lower
        or "successful" in question_lower
    ):

        if team_info is None:
            return (
                "I could not find sufficient team "
                "performance data."
            )

        matches = team_info.get(
            "matches",
            team_info.get(
                "matches_played",
                "N/A"
            )
        )

        wins = team_info.get(
            "wins",
            "N/A"
        )

        losses = team_info.get(
            "losses",
            "N/A"
        )

        win_percentage = team_info.get(
            "win_percentage",
            "N/A"
        )

        runs_scored = team_info.get(
            "runs_scored",
            "N/A"
        )

        runs_conceded = team_info.get(
            "runs_conceded",
            "N/A"
        )

        answer = (
            f"{team_name} had a strong IPL 2026 campaign. "
            f"They played {matches} matches, winning {wins} "
            f"and losing {losses}. Their win percentage was "
            f"{win_percentage}%. "
            f"They scored {runs_scored} runs and conceded "
            f"{runs_conceded} runs."
        )

        return answer

    # --------------------------------------------------------
    # Batting question
    # --------------------------------------------------------

    if (
        "bat" in question_lower
        or "batter" in question_lower
        or "runs" in question_lower
    ):

        if batting_info is None:
            return (
                "I could not find batting information "
                "for this team."
            )

        answer_parts = [
            f"The main batting contributors for "
            f"{team_name} were:"
        ]

        for _, row in batting_info.head(3).iterrows():

            player = row.get(
                "batter",
                row.get(
                    "player",
                    "Unknown"
                )
            )

            runs = row.get(
                "runs",
                "N/A"
            )

            strike_rate = row.get(
                "strike_rate",
                "N/A"
            )

            answer_parts.append(
                f"- {player}: {runs} runs "
                f"at a strike rate of {strike_rate}"
            )

        return "\n".join(answer_parts)

    # --------------------------------------------------------
    # Bowling question
    # --------------------------------------------------------

    if (
        "bowl" in question_lower
        or "wicket" in question_lower
        or "bowler" in question_lower
    ):

        if bowling_info is None:
            return (
                "I could not find bowling information "
                "for this team."
            )

        answer_parts = [
            f"The main bowling contributors for "
            f"{team_name} were:"
        ]

        for _, row in bowling_info.head(3).iterrows():

            player = row.get(
                "bowler",
                row.get(
                    "player",
                    "Unknown"
                )
            )

            wickets = row.get(
                "wickets",
                "N/A"
            )

            economy = row.get(
                "economy",
                "N/A"
            )

            answer_parts.append(
                f"- {player}: {wickets} wickets "
                f"at an economy of {economy}"
            )

        return "\n".join(answer_parts)

    # --------------------------------------------------------
    # Phase question
    # --------------------------------------------------------

    if (
        "phase" in question_lower
        or "powerplay" in question_lower
        or "middle" in question_lower
        or "death" in question_lower
    ):

        if phase_info is None or phase_info.empty:
            return (
                "I could not find phase-performance "
                "information for this team."
            )

        answer_parts = [
            f"Phase performance for {team_name}:"
        ]

        for _, row in phase_info.iterrows():

            phase = row.get(
                "phase",
                "Unknown"
            )

            runs = row.get(
                "runs",
                "N/A"
            )

            run_rate = row.get(
                "run_rate",
                "N/A"
            )

            answer_parts.append(
                f"- {phase}: {runs} runs "
                f"at a run rate of {run_rate}"
            )

        return "\n".join(answer_parts)

    # --------------------------------------------------------
    # Default answer
    # --------------------------------------------------------

    if team_info is not None:

        wins = team_info.get(
            "wins",
            "N/A"
        )

        win_percentage = team_info.get(
            "win_percentage",
            "N/A"
        )

        return (
            f"I retrieved IPL 2026 information for "
            f"{team_name}. They recorded {wins} wins "
            f"with a win percentage of {win_percentage}%. "
            f"Try asking about their batting, bowling, "
            f"phase performance, or overall performance."
        )

    return (
        "I could not find enough IPL 2026 information "
        "to answer that question."
    )


# ------------------------------------------------------------
# 11. Main program
# ------------------------------------------------------------

print("=" * 65)
print("IPL 2026 LOCAL RAG ANALYTICS ASSISTANT")
print("=" * 65)

print("\nLoading IPL 2026 analytics data...")

data = load_data()

print("Data loading completed.")


# ------------------------------------------------------------
# 12. Show available teams
# ------------------------------------------------------------

print("\nAvailable teams:")

if data["team"] is not None:

    team_column = None

    for column in ["team", "batting_team"]:

        if column in data["team"].columns:
            team_column = column
            break

    if team_column:

        teams = sorted(
            data["team"][team_column]
            .dropna()
            .astype(str)
            .unique()
        )

        for team in teams:
            print(f"- {team}")


# ------------------------------------------------------------
# 13. User input
# ------------------------------------------------------------

team_name = input(
    "\nEnter a team name: "
).strip()

question = input(
    "Ask a question about this team: "
).strip()


# ------------------------------------------------------------
# 14. Retrieve context
# ------------------------------------------------------------

print("\nRetrieving relevant IPL 2026 data...")

context = create_context(
    team_name,
    data
)

print("\n" + "=" * 65)
print("RETRIEVED GROUNDED CONTEXT")
print("=" * 65)

print(context)


# ------------------------------------------------------------
# 15. Generate answer
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("LOCAL AI ANALYTICS ANSWER")
print("=" * 65)

answer = generate_local_answer(
    question,
    team_name,
    data
)

print(answer)


# ------------------------------------------------------------
# 16. Completion message
# ------------------------------------------------------------

print("\n" + "=" * 65)
print("LOCAL RAG ANALYTICS ASSISTANT COMPLETED SUCCESSFULLY.")
print("=" * 65)