import streamlit as st
import pandas as pd
import joblib
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="IPL 2026 Analytics & AI",
    page_icon="🏏",
    layout="wide"
)
# --------------------------------------------------
# PROJECT INTRODUCTION
# --------------------------------------------------


st.title("🏏 IPL 2026 Analytics & AI Platform")

st.write(
    "An end-to-end cricket analytics platform built using "
    "Python, SQL, Excel, Power BI, Machine Learning, RAG and Streamlit."
)

st.caption(
    "Explore team performance, player statistics, match analytics, "
    "ML-based predictions and AI-powered insights."
)
# --------------------------------------------------
# PROJECT PATH
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "processed"

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------
@st.cache_data
def load_data():
    team = pd.read_csv(PROCESSED / "team_metrics_2026.csv")
    batting = pd.read_csv(PROCESSED / "batting_metrics_2026.csv")
    bowling = pd.read_csv(PROCESSED / "bowling_metrics_2026.csv")
    matches = pd.read_csv(PROCESSED / "matches_2026.csv")
    venue = pd.read_csv(PROCESSED / "venue_analytics_2026.csv")
    match_analytics = pd.read_csv(PROCESSED / "match_analytics_2026.csv")
    player_impact = pd.read_csv(PROCESSED / "player_impact_2026.csv")
    phase = pd.read_csv(PROCESSED / "phase_metrics_2026.csv")
    model = joblib.load(BASE_DIR / "models" / "ipl_2026_final_random_forest.pkl")

    return team, batting, bowling, matches, venue, match_analytics, player_impact, phase, model


team_df, batting_df, bowling_df, matches_df, venue_df, match_analytics_df, player_impact_df, phase_df, model = load_data()
# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.divider()

# --------------------------------------------------
# KPI SECTION
# --------------------------------------------------

total_matches = len(matches_df)
total_teams = team_df["team"].nunique()
total_runs = int(team_df["runs_scored"].sum())
total_players = batting_df["batter"].nunique()

col1, col2, col3, col4 = st.columns(4)

col1.metric("🏏 Matches", total_matches)
col2.metric("🏆 Teams", total_teams)
col3.metric("📊 Total Runs", f"{total_runs:,}")
col4.metric("👤 Players", total_players)

st.divider()

# --------------------------------------------------
# TEAM PERFORMANCE
# --------------------------------------------------

st.header("🏆 Team Performance")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Wins by Team")

    team_wins = (
        team_df[["team", "wins"]]
        .sort_values("wins", ascending=False)
        .set_index("team")
    )

    st.bar_chart(team_wins)

with col2:

    st.subheader("Win Percentage")

    team_win_pct = (
        team_df[["team", "win_percentage"]]
        .sort_values("win_percentage", ascending=False)
        .set_index("team")
    )

    st.bar_chart(team_win_pct)
# --------------------------------------------------
# TEAM EXPLORER
# --------------------------------------------------

st.divider()

st.header("🔎 Team Explorer")

selected_team = st.selectbox(
    "Select a team",
    sorted(team_df["team"].unique())
)

selected_team_data = team_df[
    team_df["team"] == selected_team
].iloc[0]

col1, col2, col3, col4, col5 = st.columns(5)

col1.metric(
    "Matches",
    int(selected_team_data["matches_played"])
)

col2.metric(
    "Wins",
    int(selected_team_data["wins"])
)

col3.metric(
    "Losses",
    int(selected_team_data["losses"])
)

col4.metric(
    "Win %",
    f"{selected_team_data['win_percentage']:.2f}%"
)

col5.metric(
    "Runs Scored",
    int(selected_team_data["runs_scored"])
)

st.subheader(f"{selected_team} — Performance Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.write("**Runs Scored:**", int(selected_team_data["runs_scored"]))
    st.write("**Runs Conceded:**", int(selected_team_data["runs_conceded"]))

with summary_col2:
    run_difference = (
        selected_team_data["runs_scored"]
        - selected_team_data["runs_conceded"]
    )

    st.write("**Run Difference:**", int(run_difference))
    st.write(
        "**Win Percentage:**",
        f"{selected_team_data['win_percentage']:.2f}%"
    )
# --------------------------------------------------
# TOP BATTERS
# --------------------------------------------------

st.divider()

st.header("🏏 Top Run Scorers")

top_batters = (
    batting_df[
        ["batter", "runs", "balls_faced", "strike_rate"]
    ]
    .sort_values("runs", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

top_batters.index = top_batters.index + 1

st.dataframe(
    top_batters,
    use_container_width=True
)
# --------------------------------------------------
# PLAYER ANALYSIS
# --------------------------------------------------

st.divider()

st.header("👤 Player Analysis")

selected_player = st.selectbox(
    "Select a player",
    sorted(batting_df["batter"].unique())
)

selected_player_data = batting_df[
    batting_df["batter"] == selected_player
].iloc[0]

player_col1, player_col2, player_col3, player_col4 = st.columns(4)

player_col1.metric(
    "Runs",
    int(selected_player_data["runs"])
)

player_col2.metric(
    "Balls Faced",
    int(selected_player_data["balls_faced"])
)

player_col3.metric(
    "Strike Rate",
    f"{selected_player_data['strike_rate']:.2f}"
)

player_col4.metric(
    "Fours",
    int(selected_player_data["fours"])
)

st.subheader(f"{selected_player} — Batting Summary")

player_summary_col1, player_summary_col2 = st.columns(2)

with player_summary_col1:
    st.write(
        "**Sixes:**",
        int(selected_player_data["sixes"])
    )

    st.write(
        "**Boundary Runs:**",
        int(selected_player_data["boundary_runs"])
    )

    st.write(
        "**Boundary %:**",
        f"{selected_player_data['boundary_percentage']:.2f}%"
    )

with player_summary_col2:
    st.write(
        "**Dot Balls:**",
        int(selected_player_data["dot_balls"])
    )

    st.write(
        "**Dot Ball %:**",
        f"{selected_player_data['dot_ball_percentage']:.2f}%"
    )

    st.write(
        "**Fours:**",
        int(selected_player_data["fours"])
    )
# --------------------------------------------------
# TOP BOWLERS
# --------------------------------------------------

st.header("🎯 Top Wicket Takers")

top_bowlers = (
    bowling_df[
        ["bowler", "wickets", "economy"]
    ]
    .sort_values("wickets", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

top_bowlers.index = top_bowlers.index + 1

st.dataframe(
    top_bowlers,
    use_container_width=True
)
# --------------------------------------------------
# VENUE ANALYSIS
# --------------------------------------------------

st.divider()

st.header("📍 Venue Analysis")

selected_venue = st.selectbox(
    "Select a venue",
    sorted(venue_df["venue"].unique())
)

selected_venue_data = venue_df[
    venue_df["venue"] == selected_venue
].iloc[0]

venue_col1, venue_col2, venue_col3, venue_col4 = st.columns(4)

venue_col1.metric(
    "Matches Played",
    int(selected_venue_data["matches_played"])
)

venue_col2.metric(
    "Avg First Innings",
    f"{selected_venue_data['average_first_innings_score']:.1f}"
)

venue_col3.metric(
    "Avg Match Runs",
    f"{selected_venue_data['average_match_runs']:.1f}"
)

venue_col4.metric(
    "Chase Success %",
    f"{selected_venue_data['chase_success_percentage']:.2f}%"
)

st.subheader(f"{selected_venue} — Performance")

venue_summary = pd.DataFrame({
    "Metric": [
        "City",
        "Highest Match Score",
        "Chases Won",
        "Matches Defended"
    ],
    "Value": [
        selected_venue_data["city"],
        selected_venue_data["highest_match_score"],
        selected_venue_data["chases_won"],
        selected_venue_data["matches_defended"]
    ]
})
venue_summary["Value"] = venue_summary["Value"].astype(str)
st.dataframe(
    venue_summary,
    hide_index=True,
    use_container_width=True
)
# --------------------------------------------------
# MATCH ANALYSIS
# --------------------------------------------------

st.divider()

st.header("🏏 Match Explorer")

match_options = (
    match_analytics_df["match_id"]
    .astype(str)
    + " — "
    + match_analytics_df["team1"]
    + " vs "
    + match_analytics_df["team2"]
)

selected_match = st.selectbox(
    "Select a match",
    match_options
)

selected_match_id = selected_match.split(" — ")[0]

selected_match_data = match_analytics_df[
    match_analytics_df["match_id"].astype(str) == selected_match_id
].iloc[0]

st.subheader(
    f"{selected_match_data['team1']} vs {selected_match_data['team2']}"
)

match_col1, match_col2, match_col3, match_col4 = st.columns(4)

match_col1.metric(
    "First Innings",
    int(selected_match_data["first_innings_runs"])
)

match_col2.metric(
    "Second Innings",
    int(selected_match_data["second_innings_runs"])
)

match_col3.metric(
    "Total Match Runs",
    int(selected_match_data["total_match_runs"])
)

match_col4.metric(
    "Result",
    selected_match_data["result_type"]
)

match_details = pd.DataFrame({
    "Metric": [
        "Match Date",
        "First Innings Team",
        "Second Innings Team",
        "Winner",
        "Run Margin",
        "Wicket Margin"
    ],
    "Value": [
        str(selected_match_data["match_date"]),
        str(selected_match_data["first_innings_team"]),
        str(selected_match_data["second_innings_team"]),
        str(selected_match_data["winner"]),
        str(selected_match_data["run_margin"]),
        str(selected_match_data["wickets_margin"])
    ]
})

st.dataframe(
    match_details,
    hide_index=True,
    use_container_width=True
)
# --------------------------------------------------
# AI ANALYTICS ASSISTANT
# --------------------------------------------------

st.divider()

st.header("🤖 IPL AI Analytics Assistant")
st.write(
    "Select a supported IPL 2026 analytics question. "
    "The assistant answers only from the project's analytical datasets."
)

team_names = sorted(team_df["team"].dropna().unique())
player_names = sorted(batting_df["batter"].dropna().unique())

question_bank = {
    "Team Performance": [
        "How did the selected team perform in IPL 2026?",
        "How many matches did the selected team play?",
        "How many matches did the selected team win?",
        "What is the selected team's win percentage?",
        "How many runs did the selected team score?",
        "How many runs did the selected team concede?",
    ],
    "Batting": [
        "Who scored the most runs?",
        "Who are the top 5 run scorers?",
        "Who hit the most sixes?",
        "Who hit the most fours?",
        "What was the selected player's strike rate?",
        "How many runs did the selected player score?",
    ],
    "Bowling": [
        "Who took the most wickets?",
        "Who are the top 5 wicket takers?",
        "Who had the best economy rate?",
        "Who had the best bowling strike rate?",
        "What was the selected player's economy rate?",
        "How many wickets did the selected player take?",
    ],
    "Phase Analysis": [
        "Which phase had the most runs?",
        "How did the selected team perform across phases?",
        "How did the selected team perform in the powerplay?",
        "How did the selected team perform in the middle overs?",
        "How did the selected team perform in the death overs?",
    ],
    "Venue Analysis": [
        "Which venue had the highest average match score?",
        "Which venue had the highest match score?",
        "Which venue had the best chase success?",
    ],
    "Match Analysis": [
        "Which was the highest-scoring match?",
        "How many matches were won by chasing?",
        "How many matches were defended?",
    ],
    "Team Comparison": [
        "Which team had the highest win percentage?",
        "Which team scored the most runs?",
        "Which team conceded the most runs?",
        "Compare two teams",
    ],
}

category = st.selectbox(
    "1. Select question category",
    list(question_bank.keys()),
    key="ai_category"
)

selected_question = st.selectbox(
    "2. Select your question",
    question_bank[category],
    key="ai_question"
)

selected_team_for_ai = None
selected_player_for_ai = None

if category in ["Team Performance", "Phase Analysis"]:
    selected_team_for_ai = st.selectbox(
        "Select team",
        team_names,
        key="ai_team"
    )

if selected_question in [
    "What was the selected player's strike rate?",
    "How many runs did the selected player score?",
    "What was the selected player's economy rate?",
    "How many wickets did the selected player take?",
]:
    selected_player_for_ai = st.selectbox(
        "Select player",
        player_names,
        key="ai_player"
    )

comparison_team1 = None
comparison_team2 = None
if selected_question == "Compare two teams":
    comparison_team1 = st.selectbox("Select Team 1", team_names, key="ai_compare_team1")
    comparison_team2 = st.selectbox("Select Team 2", team_names, key="ai_compare_team2")

if st.button("🔍 Generate Insight", key="generate_ai_insight"):

    # --------------------------------------------------
    # TEAM PERFORMANCE
    # --------------------------------------------------
    if category == "Team Performance":
        row = team_df[team_df["team"] == selected_team_for_ai].iloc[0]
        st.success(f"### 📊 {selected_team_for_ai} — IPL 2026")

        if selected_question == "How did the selected team perform in IPL 2026?":
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Matches", int(row["matches_played"]))
            c2.metric("Wins", int(row["wins"]))
            c3.metric("Losses", int(row["losses"]))
            c4.metric("Win %", f"{row['win_percentage']:.2f}%")
            st.write(
                f"{selected_team_for_ai} played **{int(row['matches_played'])} matches**, "
                f"winning **{int(row['wins'])}** and losing **{int(row['losses'])}**. "
                f"The team scored **{int(row['runs_scored']):,} runs** and conceded "
                f"**{int(row['runs_conceded']):,} runs**."
            )
        elif selected_question == "How many matches did the selected team play?":
            st.success(f"{selected_team_for_ai} played **{int(row['matches_played'])} matches**.")
        elif selected_question == "How many matches did the selected team win?":
            st.success(f"{selected_team_for_ai} won **{int(row['wins'])} matches**.")
        elif selected_question == "What is the selected team's win percentage?":
            st.success(f"{selected_team_for_ai}'s win percentage was **{row['win_percentage']:.2f}%**.")
        elif selected_question == "How many runs did the selected team score?":
            st.success(f"{selected_team_for_ai} scored **{int(row['runs_scored']):,} runs**.")
        elif selected_question == "How many runs did the selected team concede?":
            st.success(f"{selected_team_for_ai} conceded **{int(row['runs_conceded']):,} runs**.")

    # --------------------------------------------------
    # BATTING
    # --------------------------------------------------
    elif category == "Batting":
        if selected_question in ["Who scored the most runs?", "Who are the top 5 run scorers?"]:
            result = batting_df.sort_values("runs", ascending=False).head(5)
            st.write("### 🏏 Top Run Scorers")
            st.dataframe(result[["batter", "runs", "balls_faced", "strike_rate"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['batter']} was the leading run scorer with **{int(top['runs'])} runs**.")
        elif selected_question == "Who hit the most sixes?":
            result = batting_df.sort_values("sixes", ascending=False).head(5)
            st.write("### 🏏 Most Sixes")
            st.dataframe(result[["batter", "sixes", "runs"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['batter']} hit the most sixes, with **{int(top['sixes'])} sixes**.")
        elif selected_question == "Who hit the most fours?":
            result = batting_df.sort_values("fours", ascending=False).head(5)
            st.write("### 🏏 Most Fours")
            st.dataframe(result[["batter", "fours", "runs"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['batter']} hit the most fours, with **{int(top['fours'])} fours**.")
        elif selected_question == "What was the selected player's strike rate?":
            row = batting_df[batting_df["batter"] == selected_player_for_ai].iloc[0]
            st.success(f"**{selected_player_for_ai}** had a strike rate of **{row['strike_rate']:.2f}**.")
        elif selected_question == "How many runs did the selected player score?":
            row = batting_df[batting_df["batter"] == selected_player_for_ai].iloc[0]
            st.success(f"**{selected_player_for_ai}** scored **{int(row['runs'])} runs**.")

    # --------------------------------------------------
    # BOWLING
    # --------------------------------------------------
    elif category == "Bowling":
        if selected_question in ["Who took the most wickets?", "Who are the top 5 wicket takers?"]:
            result = bowling_df.sort_values("wickets", ascending=False).head(5)
            st.write("### 🎯 Top Wicket Takers")
            st.dataframe(result[["bowler", "wickets", "economy"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['bowler']} was the leading wicket taker with **{int(top['wickets'])} wickets**.")
        elif selected_question == "Who had the best economy rate?":
            result = bowling_df.sort_values("economy", ascending=True).head(5)
            st.write("### 🎯 Best Economy Rates")
            st.dataframe(result[["bowler", "economy", "wickets"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['bowler']} recorded the best economy rate among the listed bowlers at **{top['economy']:.2f}**.")
        elif selected_question == "Who had the best bowling strike rate?":
            result = bowling_df.sort_values("bowling_strike_rate", ascending=True).head(5)
            st.write("### 🎯 Best Bowling Strike Rates")
            st.dataframe(result[["bowler", "bowling_strike_rate", "wickets"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['bowler']} had the best bowling strike rate among the listed bowlers at **{top['bowling_strike_rate']:.2f} balls per wicket**.")
        elif selected_question == "What was the selected player's economy rate?":
            row = bowling_df[bowling_df["bowler"] == selected_player_for_ai].iloc[0]
            st.success(f"**{selected_player_for_ai}** had an economy rate of **{row['economy']:.2f}**.")
        elif selected_question == "How many wickets did the selected player take?":
            row = bowling_df[bowling_df["bowler"] == selected_player_for_ai].iloc[0]
            st.success(f"**{selected_player_for_ai}** took **{int(row['wickets'])} wickets**.")

    # --------------------------------------------------
    # PHASE ANALYSIS
    # --------------------------------------------------
    elif category == "Phase Analysis":
        result = phase_df[phase_df["batting_team"] == selected_team_for_ai].copy()
        if selected_question == "How did the selected team perform across phases?":
            result = result.sort_values("runs", ascending=False)
        elif selected_question == "How did the selected team perform in the powerplay?":
            result = result[result["phase"].str.lower() == "powerplay"]
        elif selected_question == "How did the selected team perform in the middle overs?":
            result = result[result["phase"].str.lower() == "middle"]
        elif selected_question == "How did the selected team perform in the death overs?":
            result = result[result["phase"].str.lower() == "death"]
        else:
            result = phase_df.groupby("phase", as_index=False)["runs"].sum().sort_values("runs", ascending=False)

        st.write("### 📈 Phase Performance")
        st.dataframe(result[["phase", "runs", "run_rate", "wickets"]], hide_index=True, use_container_width=True)
        if not result.empty:
            top_phase = result.sort_values("runs", ascending=False).iloc[0]
            st.write(
                f"**💡 Insight:** {selected_team_for_ai} scored the most runs in the **{top_phase['phase']}**, "
                f"with **{int(top_phase['runs'])} runs** at a run rate of **{top_phase['run_rate']:.2f}**."
            )

    # --------------------------------------------------
    # VENUE ANALYSIS
    # --------------------------------------------------
    elif category == "Venue Analysis":
        if selected_question == "Which venue had the highest average match score?":
            result = venue_df.sort_values("average_match_runs", ascending=False).head(5)
            st.write("### 🏟️ Highest Average Match Scores")
            st.dataframe(result[["venue", "average_match_runs", "matches_played"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['venue']} had the highest average match score among the listed venues at **{top['average_match_runs']:.2f} runs**.")
        elif selected_question == "Which venue had the highest match score?":
            result = venue_df.sort_values("highest_match_score", ascending=False).head(5)
            st.write("### 🏟️ Highest Match Scores")
            st.dataframe(result[["venue", "highest_match_score"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** The highest match score recorded at a venue was **{int(top['highest_match_score'])} runs** at **{top['venue']}**.")
        else:
            result = venue_df.sort_values("chase_success_percentage", ascending=False).head(5)
            st.write("### 🏟️ Best Chase Success by Venue")
            st.dataframe(result[["venue", "matches_played", "chases_won", "chase_success_percentage"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['venue']} had the highest chase success percentage among the listed venues at **{top['chase_success_percentage']:.2f}%**.")

    # --------------------------------------------------
    # MATCH ANALYSIS
    # --------------------------------------------------
    elif category == "Match Analysis":
        if selected_question == "Which was the highest-scoring match?":
            result = match_analytics_df.sort_values("total_match_runs", ascending=False).head(5)
            st.write("### 🔥 Highest-Scoring Matches")
            st.dataframe(result[["match_id", "team1", "team2", "first_innings_runs", "second_innings_runs", "total_match_runs", "winner"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** The highest-scoring match was **{top['team1']} vs {top['team2']}**, producing **{int(top['total_match_runs'])} total runs**.")
        elif selected_question == "How many matches were won by chasing?":
            count = int((match_analytics_df["result_type"] == "Chased").sum())
            st.success(f"**{count} completed matches** were won by chasing in IPL 2026.")
            st.write("**💡 Insight:** Chasing was the winning strategy in a substantial share of the completed matches.")
        else:
            count = int((match_analytics_df["result_type"] == "Defended").sum())
            st.success(f"**{count} completed matches** were won by defending in IPL 2026.")
            st.write("**💡 Insight:** Defending was the winning strategy in the remaining completed matches classified as defended.")

    # --------------------------------------------------
    # TEAM COMPARISON
    # --------------------------------------------------
    elif category == "Team Comparison":
        if selected_question == "Which team had the highest win percentage?":
            result = team_df.sort_values("win_percentage", ascending=False).head(5)
            st.write("### 🏆 Highest Win Percentages")
            st.dataframe(result[["team", "wins", "losses", "win_percentage"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['team']} had the highest win percentage among the teams at **{top['win_percentage']:.2f}%**.")
        elif selected_question == "Which team scored the most runs?":
            result = team_df.sort_values("runs_scored", ascending=False).head(5)
            st.write("### 🏏 Teams with Most Runs")
            st.dataframe(result[["team", "runs_scored"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['team']} scored the most runs, with **{int(top['runs_scored']):,} runs**.")
        elif selected_question == "Which team conceded the most runs?":
            result = team_df.sort_values("runs_conceded", ascending=False).head(5)
            st.write("### 🎯 Teams with Most Runs Conceded")
            st.dataframe(result[["team", "runs_conceded"]], hide_index=True, use_container_width=True)
            top = result.iloc[0]
            st.write(f"**💡 Insight:** {top['team']} conceded the most runs, with **{int(top['runs_conceded']):,} runs**.")
        else:
            if comparison_team1 == comparison_team2:
                st.warning("Please select two different teams.")
            else:
                a = team_df[team_df["team"] == comparison_team1].iloc[0]
                b = team_df[team_df["team"] == comparison_team2].iloc[0]
                comparison = pd.DataFrame({
                    "Metric": ["Matches", "Wins", "Losses", "Win %", "Runs Scored", "Runs Conceded"],
                    comparison_team1: [int(a["matches_played"]), int(a["wins"]), int(a["losses"]), round(a["win_percentage"], 2), int(a["runs_scored"]), int(a["runs_conceded"])],
                    comparison_team2: [int(b["matches_played"]), int(b["wins"]), int(b["losses"]), round(b["win_percentage"], 2), int(b["runs_scored"]), int(b["runs_conceded"])],
                })
                st.write(f"### ⚔️ {comparison_team1} vs {comparison_team2}")
                st.dataframe(comparison, hide_index=True, use_container_width=True)
                better = comparison_team1 if a["win_percentage"] >= b["win_percentage"] else comparison_team2
                st.write(
                    f"**💡 Insight:** Based on win percentage, **{better}** performed better between the two selected teams."
                )

    st.info("Response generated only from the IPL 2026 analytical datasets used by the project.")

# ML MATCH PREDICTION
# --------------------------------------------------

st.divider()

st.header("🤖 ML Match Prediction")

st.write(
    "Predict the likely winner of an IPL 2026 match using the trained Random Forest model."
)

prediction_col1, prediction_col2 = st.columns(2)

with prediction_col1:
    prediction_team1 = st.selectbox(
        "Select Team 1",
        sorted(team_df["team"].unique()),
        key="prediction_team1"
    )

with prediction_col2:
    prediction_team2 = st.selectbox(
        "Select Team 2",
        sorted(team_df["team"].unique()),
        key="prediction_team2"
    )

if prediction_team1 == prediction_team2:
    st.warning("Please select two different teams.")
else:
    if st.button("🔮 Predict Winner", key="predict_winner"):

        # Use overall team performance as the pre-match baseline
        team1_row = team_df[team_df["team"] == prediction_team1].iloc[0]
        team2_row = team_df[team_df["team"] == prediction_team2].iloc[0]

        input_data = pd.DataFrame([{
            "team1": prediction_team1,
            "team2": prediction_team2,
            "venue": "Narendra Modi Stadium",
            "team1_prev_win_pct": team1_row["win_percentage"],
            "team2_prev_win_pct": team2_row["win_percentage"],
            "team1_recent_form": team1_row["win_percentage"],
            "team2_recent_form": team2_row["win_percentage"],
           "team1_avg_runs": team1_row["runs_scored"] / team1_row["matches_played"],
            "team2_avg_runs": team2_row["runs_scored"] / team2_row["matches_played"],
           "team1_avg_conceded": team1_row["runs_conceded"] / team1_row["matches_played"],
           "team2_avg_conceded": team2_row["runs_conceded"] / team2_row["matches_played"],
            "toss_winner_is_team1": 0,
            "toss_decision": "field"
        }])

        prediction = model.predict(input_data)[0]
        probabilities = model.predict_proba(input_data)[0]

        if prediction == 1:
            predicted_winner = prediction_team1
        else:
            predicted_winner = prediction_team2

        st.success(f"🏆 Predicted Winner: {predicted_winner}")

        result_col1, result_col2 = st.columns(2)

        with result_col1:
            st.metric(
                prediction_team1,
                f"{probabilities[1] * 100:.2f}%"
            )

        with result_col2:
            st.metric(
                prediction_team2,
                f"{probabilities[0] * 100:.2f}%"
            )
# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "IPL 2026 Analytics & AI | Built with Python, SQL, Power BI, "
    "Machine Learning, RAG and Streamlit"
)