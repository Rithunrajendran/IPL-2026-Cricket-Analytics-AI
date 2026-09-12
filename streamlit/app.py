import streamlit as st
import pandas as pd
import numpy as np
import joblib
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    page_title="IPL 2026 Analytics",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ─────────────────────────────────────────────
# SIMPLE PALETTE
# ─────────────────────────────────────────────
# Background : #f8f9fa (light gray)
# Surface    : #ffffff (white)
# Border     : #dee2e6 (gray-300)
# Text dark  : #212529
# Text muted : #6c757d
# Accent     : #2563eb (blue)
# Accent-dim : #dbeafe (light blue)
# Sidebar bg : #f1f3f5

# ─────────────────────────────────────────────
# GLOBAL CSS  — simple, no gradients, no glows
# ─────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
* { font-family: 'Inter', sans-serif; box-sizing: border-box; }

/* ── BASE ── */
[data-testid="stAppViewContainer"],
[data-testid="stMain"] { background: #f8f9fa; }
.block-container { padding: 0 0 2rem 0 !important; max-width: 100% !important; }

/* ── TEXT ── */
h1,h2,h3,h4,h5,p,label,
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] h1,
[data-testid="stMarkdownContainer"] h2,
[data-testid="stMarkdownContainer"] h3 { color: #212529 !important; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #f1f3f5 !important;
    border-right: 1px solid #dee2e6 !important;
    transition: width 0.3s ease !important;
}
[data-testid="stSidebar"] * { color: #212529 !important; }
[data-testid="stSidebar"] [data-testid="stVerticalBlock"] { gap: 0 !important; padding: 0 !important; }
[data-testid="stSidebar"] .stButton > button {
    background: transparent !important;
    color: #212529 !important;
    border: none !important;
    border-radius: 8px !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    text-align: left !important;
    padding: 0.6rem 1rem !important;
    width: 100% !important;
    box-shadow: none !important;
    transform: none !important;
    justify-content: flex-start !important;
}
[data-testid="stSidebar"] .stButton > button:hover {
    background: #e9ecef !important;
    transform: none !important;
    box-shadow: none !important;
}
/* Active nav item highlight */
[data-testid="stSidebar"] .stButton > button[kind="secondary"]:focus {
    background: #dbeafe !important;
    color: #2563eb !important;
    border-left: 3px solid #2563eb !important;
    border-radius: 0 8px 8px 0 !important;
}

/* ── HIDE DEPLOY BUTTON & STREAMLIT TOOLBAR ── */
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"],
#MainMenu,
header { visibility: hidden !important; height: 0 !important; }

/* ── MAIN CONTENT: fills remaining space when sidebar collapses/expands ── */
[data-testid="stAppViewContainer"] {
    display: flex !important;
    flex-direction: row !important;
    flex-wrap: nowrap !important;
    width: 100vw !important;
}
[data-testid="stMain"] {
    flex: 1 1 0 !important;
    min-width: 0 !important;
    overflow-x: hidden !important;
    transition: all 0.3s ease !important;
}
.block-container { min-width: 0 !important; }

/* ── TOUR CARD ── */
.tour-card {
    background: #ffffff;
    border-radius: 14px;
    border: 1px solid #dee2e6;
    padding: 2rem 2.2rem;
    box-shadow: 0 4px 24px rgba(0,0,0,0.08);
    margin-top: 4rem;
}
.tour-step-label {
    font-size: 0.68rem; font-weight: 700; color: #6c757d;
    text-transform: uppercase; letter-spacing: 1px; margin-bottom: 0.5rem;
}
.tour-title {
    font-size: 1.3rem; font-weight: 800; color: #212529; margin-bottom: 0.7rem;
}
.tour-title span { color: #2563eb; }
.tour-body {
    font-size: 0.9rem; color: #495057; line-height: 1.65; margin-bottom: 1.4rem;
}
.tour-progress {
    display: flex; gap: 5px; margin-bottom: 1.2rem;
}
.tour-dot {
    height: 5px; border-radius: 999px; background: #dee2e6; flex: 1;
}
.tour-dot.active { background: #2563eb; }
.tour-dot.done   { background: #93c5fd; }

/* ── METRICS ── */
[data-testid="stMetric"] {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 10px;
    padding: 0.9rem 1rem;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
}
[data-testid="stMetricLabel"] {
    color: #6c757d !important;
    font-size: 0.72rem !important;
    font-weight: 700 !important;
    text-transform: uppercase;
    letter-spacing: 0.6px;
}
[data-testid="stMetricValue"] {
    color: #2563eb !important;
    font-weight: 800 !important;
    font-size: 1.5rem !important;
}

/* ── WIDGETS ── */
[data-testid="stWidgetLabel"] p { color: #6c757d !important; font-size: 0.82rem !important; }
.stSelectbox div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border-color: #dee2e6 !important;
    color: #212529 !important;
    border-radius: 8px !important;
}

/* ── TABS ── */
[data-testid="stTabs"] [role="tablist"] { border-bottom: 1px solid #dee2e6; gap: 4px; }
[data-testid="stTabs"] button {
    color: #6c757d !important;
    font-weight: 700 !important;
    border-radius: 6px 6px 0 0 !important;
    padding: 0.4rem 1rem !important;
    font-size: 0.85rem !important;
}
[data-testid="stTabs"] button[aria-selected="true"] {
    color: #2563eb !important;
    border-bottom: 2px solid #2563eb !important;
    background: #dbeafe !important;
}

/* ── BUTTONS ── */
.stButton > button {
    background: #2563eb;
    color: #ffffff !important;
    border: none;
    border-radius: 8px;
    font-weight: 700;
    padding: 0.45rem 1.4rem;
    box-shadow: none;
    transition: background 0.15s;
}
.stButton > button:hover { background: #1d4ed8; }

/* Tour Back / Skip buttons — secondary style */
button[data-testid="baseButton-secondary"][kind="secondary"],
div[data-testid="stButton"] > button[key="tour_back"],
div[data-testid="stButton"] > button[key="tour_skip"] {
    background: #f1f3f5 !important;
    color: #495057 !important;
    border: 1px solid #dee2e6 !important;
}
div[data-testid="stButton"] > button[key="tour_back"]:hover,
div[data-testid="stButton"] > button[key="tour_skip"]:hover {
    background: #e9ecef !important;
}

/* ── DATAFRAME ── */
[data-testid="stDataFrame"] {
    border-radius: 8px;
    overflow: hidden;
    border: 1px solid #dee2e6;
}

/* ── SCROLLBAR ── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: #f1f3f5; }
::-webkit-scrollbar-thumb { background: #adb5bd; border-radius: 999px; }

/* ── HERO ── */
.hero-wrap {
    background: #ffffff;
    padding: 2rem 2.5rem;
    border-bottom: 1px solid #dee2e6;
}
.hero-eyebrow {
    display: inline-block;
    background: #dbeafe;
    color: #1e40af;
    font-size: 0.7rem;
    font-weight: 700;
    padding: 0.2rem 0.75rem;
    border-radius: 999px;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}
.hero-title {
    font-size: 2.4rem;
    font-weight: 800;
    color: #212529;
    letter-spacing: -1px;
    line-height: 1.1;
    margin-bottom: 0.35rem;
}
.hero-title span { color: #2563eb; }
.hero-sub { font-size: 0.95rem; color: #6c757d; margin-bottom: 1rem; }
.hero-tags { display: flex; gap: 0.4rem; flex-wrap: wrap; }
.hero-tag {
    background: #f1f3f5;
    border: 1px solid #dee2e6;
    padding: 0.25rem 0.7rem;
    border-radius: 999px;
    font-size: 0.78rem;
    color: #495057;
    font-weight: 600;
}

/* ── KPI STRIP ── */
.kpi-strip {
    display: flex;
    flex-wrap: nowrap;
    background: #f8f9fa;
    border-bottom: 1px solid #dee2e6;
    border-top: 1px solid #dee2e6;
    overflow: hidden;
}
.kpi-item {
    flex: 1;
    min-width: 0;
    padding: 0.75rem 1rem;
    border-right: 1px solid #dee2e6;
}
.kpi-item:last-child { border-right: none; }
.kpi-num  { font-size: 1.1rem; font-weight: 800; color: #2563eb; line-height: 1; white-space: nowrap; }
.kpi-lbl  { font-size: 0.58rem; color: #6c757d; text-transform: uppercase; letter-spacing: 0.6px; font-weight: 700; margin-top: 2px; white-space: nowrap; }

/* ── SECTION ── */
.sec-wrap { padding: 1.6rem 2.5rem; }
.sec-head { font-size: 1.2rem; font-weight: 800; color: #212529 !important; margin-bottom: 0.1rem; }
.sec-head span { color: #2563eb; }
.sec-sub  { font-size: 0.82rem; color: #6c757d !important; margin-bottom: 1rem; }

/* ── STAR / PLAYER CARDS ── */
.star-card {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 12px;
    padding: 1rem;
    text-align: center;
    box-shadow: 0 1px 4px rgba(0,0,0,0.06);
    min-height: 150px;
}
.star-card-badge { font-size: 0.65rem; font-weight: 700; text-transform: uppercase; letter-spacing: 0.8px; margin-bottom: 0.4rem; color: #6c757d; }
.star-initials {
    width: 48px; height: 48px; border-radius: 50%;
    margin: 0 auto 0.5rem auto;
    display: flex; align-items: center; justify-content: center;
    font-size: 0.9rem; font-weight: 800;
    background: #dbeafe; color: #1e40af;
}
.star-name  { font-size: 0.82rem; font-weight: 700; color: #212529; margin-bottom: 0.15rem; }
.star-stat  { font-size: 1.3rem; font-weight: 800; color: #2563eb; line-height: 1; }
.star-label { font-size: 0.62rem; color: #6c757d; text-transform: uppercase; letter-spacing: 0.6px; font-weight: 700; }

/* ── HIGHLIGHT CARD ── */
.hl-card {
    background: #ffffff;
    border: 1px solid #dee2e6;
    border-radius: 10px;
    padding: 0.85rem 1rem;
    margin-bottom: 0.5rem;
}
.hl-title { font-size: 0.78rem; font-weight: 700; color: #2563eb; text-transform: uppercase; letter-spacing: 0.5px; }
.hl-val   { font-size: 1rem; font-weight: 800; color: #212529; }
.hl-sub   { font-size: 0.7rem; color: #6c757d; }

/* ── INSIGHT BOX ── */
.insight-box {
    background: #dbeafe;
    border-left: 3px solid #2563eb;
    border-radius: 0 8px 8px 0;
    padding: 0.65rem 1rem;
    margin-top: 0.6rem;
    color: #1e40af !important;
    font-size: 0.88rem;
    font-weight: 500;
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    padding: 1.2rem 0;
    border-top: 1px solid #dee2e6;
    color: #adb5bd;
    font-size: 0.75rem;
    margin-top: 2rem;
    background: #ffffff;
}
.footer a { color: #6c757d; text-decoration: none; margin: 0 0.5rem; }
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# PATHS & DATA
# ─────────────────────────────────────────────
BASE_DIR  = Path(__file__).resolve().parent.parent
PROCESSED = BASE_DIR / "processed"

@st.cache_data
def load_data():
    team     = pd.read_csv(PROCESSED / "team_metrics_2026.csv")
    batting  = pd.read_csv(PROCESSED / "batting_metrics_2026.csv")
    bowling  = pd.read_csv(PROCESSED / "bowling_metrics_2026.csv")
    matches  = pd.read_csv(PROCESSED / "matches_2026.csv")
    venue    = pd.read_csv(PROCESSED / "venue_analytics_2026.csv")
    match_an = pd.read_csv(PROCESSED / "match_analytics_2026.csv")
    player_i = pd.read_csv(PROCESSED / "player_impact_2026.csv")
    phase    = pd.read_csv(PROCESSED / "phase_metrics_2026.csv")
    ml_model = joblib.load(BASE_DIR / "models" / "ipl_2026_final_random_forest.pkl")
    return team, batting, bowling, matches, venue, match_an, player_i, phase, ml_model

team_df, batting_df, bowling_df, matches_df, venue_df, match_df, player_impact_df, phase_df, model = load_data()

# ─────────────────────────────────────────────
# PLOTLY THEME  — simple light palette
# ─────────────────────────────────────────────
PLOT_BG  = "#ffffff"
FONT_COL = "#212529"
GRID_COL = "#e9ecef"
BLUE     = "#2563eb"
BLUE2    = "#60a5fa"
BLUE_SEQ = ["#dbeafe","#93c5fd","#60a5fa","#3b82f6","#2563eb","#1d4ed8","#1e40af","#1e3a8a"]

def base_layout(**kw):
    title_val  = kw.pop("title",  "")
    xaxis_over = kw.pop("xaxis",  {})
    yaxis_over = kw.pop("yaxis",  {})
    bx = dict(gridcolor=GRID_COL, linecolor=GRID_COL,
               tickfont=dict(color=FONT_COL), title_font=dict(color="#6c757d"))
    by = dict(gridcolor=GRID_COL, linecolor=GRID_COL,
               tickfont=dict(color=FONT_COL), title_font=dict(color="#6c757d"))
    bx.update(xaxis_over); by.update(yaxis_over)
    return dict(
        plot_bgcolor=PLOT_BG, paper_bgcolor=PLOT_BG,
        font=dict(color=FONT_COL, family="Inter, sans-serif", size=12),
        title=dict(text=title_val, font=dict(color=FONT_COL, size=13, family="Inter")),
        xaxis=bx, yaxis=by,
        legend=dict(bgcolor="#ffffff", font=dict(color=FONT_COL),
                    bordercolor="#dee2e6", borderwidth=1),
        margin=dict(l=8, r=8, t=36 if title_val else 12, b=8),
        hoverlabel=dict(bgcolor="#ffffff", font_color=FONT_COL,
                        bordercolor=BLUE, font_size=12),
        **kw
    )

# ─────────────────────────────────────────────
# NAVIGATION STATE
# ─────────────────────────────────────────────
PAGES = ["Overview", "Team Performance", "Player Analysis", "Bowling Stats",
         "Venue Analysis", "Match Explorer", "Data Explorer", "Match Prediction"]

if "page" not in st.session_state:
    st.session_state["page"] = "Overview"

# ─────────────────────────────────────────────
# LEFT SIDEBAR
# ─────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:1.2rem 0 1rem 0;
                border-bottom:1px solid #dee2e6;margin-bottom:0.8rem;'>
        <div style='font-size:1.1rem;font-weight:800;color:#2563eb;letter-spacing:-0.5px;'>IPL 2026</div>
        <div style='font-size:0.6rem;color:#6c757d;text-transform:uppercase;letter-spacing:2px;'>Analytics Platform</div>
    </div>
    """, unsafe_allow_html=True)

    for i, p in enumerate(PAGES, 1):
        if st.button(f"{i}. {p}", key=f"sb_{p.replace(' ','_')}", use_container_width=True):
            st.session_state["page"] = p
            st.rerun()

    st.markdown("""
    <div style='padding:0.8rem 1rem;border-top:1px solid #dee2e6;margin-top:1rem;text-align:center;'>
        <div style='font-size:0.65rem;color:#6c757d;'>Python · Streamlit</div>
    </div>
    """, unsafe_allow_html=True)

page = st.session_state["page"]

# ─────────────────────────────────────────────
# ONBOARDING TOUR
# ─────────────────────────────────────────────
TOUR_STEPS = [
    {
        "title": "Welcome to <span>IPL 2026 Analytics</span>",
        "body": (
            "This platform gives you deep cricket intelligence powered by real IPL 2026 match data. "
            "You get interactive charts, player profiles, venue breakdowns, and a statistical match predictor — all in one place.<br><br>"
            "This short tour will walk you through every section. Use the buttons below to move through it."
        ),
    },
    {
        "title": "Overview",
        "body": (
            "The <b>Overview</b> page is your season dashboard. It shows a hero banner with season context, "
            "a KPI strip with key numbers (matches, runs, teams, players, wickets, sixes), and quick-look charts "
            "for team run totals and win percentages. Season highlights — Orange Cap, Purple Cap, and Champions — are "
            "shown in a sidebar panel on the right."
        ),
    },
    {
        "title": "Team Performance",
        "body": (
            "<b>Team Performance</b> has three tabs:<br>"
            "&nbsp;&bull; <b>Season Overview</b> — bar charts for wins and a scatter showing runs scored vs conceded.<br>"
            "&nbsp;&bull; <b>Team Deep-Dive</b> — pick any team to see its win gauge, run breakdown, and phase-wise performance.<br>"
            "&nbsp;&bull; <b>Head to Head</b> — compare any two teams side by side across all key stats."
        ),
    },
    {
        "title": "Player Analysis",
        "body": (
            "<b>Player Analysis</b> covers batting in depth:<br>"
            "&nbsp;&bull; <b>Leaderboard</b> — filter by minimum balls faced, sort by runs, strike rate, sixes, fours, or boundary %, and choose Top N.<br>"
            "&nbsp;&bull; <b>Player Profile</b> — select any batter for a full breakdown: metrics, percentile radar chart, milestone scores (30+, 50+, 100+), and bowling stats if they bowl too."
        ),
    },
    {
        "title": "Bowling Stats",
        "body": (
            "<b>Bowling Stats</b> mirrors the batting section for bowlers:<br>"
            "&nbsp;&bull; <b>Leaderboard</b> — filter by minimum wickets, sort by economy, average, strike rate, or wicket hauls.<br>"
            "&nbsp;&bull; <b>Bowler Profile</b> — economy gauge, haul breakdown (3W+, 4W+, 5W+), and full stats for any bowler."
        ),
    },
    {
        "title": "Venue Analysis",
        "body": (
            "<b>Venue Analysis</b> shows ground-by-ground patterns:<br>"
            "&nbsp;&bull; <b>All Venues</b> — average match scores and a scatter of first innings vs chase success across all grounds.<br>"
            "&nbsp;&bull; <b>Venue Deep-Dive</b> — pick a ground to see a chase success gauge and a summary table with city, highest score, chases won, and matches defended."
        ),
    },
    {
        "title": "Match Explorer",
        "body": (
            "<b>Match Explorer</b> lets you dig into individual matches:<br>"
            "&nbsp;&bull; <b>All Matches</b> — run distribution histogram and a results pie chart, plus the top 10 highest-scoring matches.<br>"
            "&nbsp;&bull; <b>Match Details</b> — select any match from a dropdown to see innings scores side by side, result type, margin, and a full match summary table."
        ),
    },
    {
        "title": "Data Explorer",
        "body": (
            "The <b>Data Explorer</b> lets you query the dataset through pre-built questions — no code needed.<br><br>"
            "Pick a <b>category</b> (Team, Batting, Bowling, Phase, Venue, Match, Comparison), then choose a <b>question</b>. "
            "Some questions let you select a specific team or player. Hit <b>Generate Insight</b> and the answer renders instantly as a chart or stat."
        ),
    },
    {
        "title": "Match Prediction",
        "body": (
            "<b>Match Prediction</b> uses a trained <b>Random Forest model</b> built on IPL 2026 data.<br><br>"
            "Select two teams and click <b>Predict Winner</b>. The model uses each team's win percentage, recent form, average runs scored, "
            "and average runs conceded to output a predicted winner and win probability gauges for both sides."
        ),
    },
    {
        "title": "You're all set!",
        "body": (
            "You now know your way around the full platform. Use the <b>sidebar</b> on the left to jump between sections at any time — "
            "you can collapse it with the arrow button to get more screen space.<br><br>"
            "Click <b>Start Exploring</b> below to dive in."
        ),
    },
]

if "tour_done" not in st.session_state:
    st.session_state["tour_done"] = False
if "tour_step" not in st.session_state:
    st.session_state["tour_step"] = 0

if not st.session_state["tour_done"]:
    step    = st.session_state["tour_step"]
    total   = len(TOUR_STEPS)
    current = TOUR_STEPS[step]
    is_last = step == total - 1

    # Center the card using columns
    _, card_col, _ = st.columns([1, 2, 1])

    with card_col:
        # Progress dots
        dots_html = "".join(
            f'<div class="tour-dot {"active" if i == step else "done" if i < step else ""}"></div>'
            for i in range(total)
        )

        st.markdown(f"""
        <div class="tour-card">
            <div class="tour-step-label">Step {step + 1} of {total}</div>
            <div class="tour-title">{current['title']}</div>
            <div class="tour-progress">{dots_html}</div>
            <div class="tour-body">{current['body']}</div>
        </div>
        """, unsafe_allow_html=True)

        # Buttons in the same column so they're never obscured
        left, mid, right = st.columns([1, 1, 1])

        with left:
            if step > 0:
                if st.button("← Back", key="tour_back", use_container_width=True):
                    st.session_state["tour_step"] -= 1
                    st.rerun()

        with mid:
            if st.button("Skip tour", key="tour_skip", use_container_width=True):
                st.session_state["tour_done"] = True
                st.rerun()

        with right:
            label = "Start Exploring" if is_last else "Next →"
            if st.button(label, key="tour_next", use_container_width=True):
                if is_last:
                    st.session_state["tour_done"] = True
                else:
                    st.session_state["tour_step"] += 1
                st.rerun()

    st.stop()  # Hold the main app until tour is dismissed

# ─────────────────────────────────────────────
# HELPER FUNCTIONS
# ─────────────────────────────────────────────
def section(title, sub="", wrap=True):
    pad = '<div class="sec-wrap">' if wrap else ""
    st.markdown(f"""{pad}
    <p class="sec-head">{title}</p>
    {"<p class='sec-sub'>"+sub+"</p>" if sub else ""}
    """, unsafe_allow_html=True)

def insight(text):
    st.markdown(f'<div class="insight-box">{text}</div>', unsafe_allow_html=True)

def pct_rank(series, value):
    s = series.dropna()
    return round((s < value).sum() / len(s) * 100, 1) if len(s) else 0

def star_card(col, badge, name, stat, stat_label):
    col.markdown(f"""
    <div class="star-card">
        <div class="star-card-badge">{badge}</div>
        <div class="star-initials">{initials(name)}</div>
        <div class="star-name">{name}</div>
        <div class="star-stat">{stat}</div>
        <div class="star-label">{stat_label}</div>
    </div>""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# DERIVED DATA
# ─────────────────────────────────────────────
top_bat   = batting_df.sort_values("runs", ascending=False).iloc[0]
top_bowl  = bowling_df.sort_values("wickets", ascending=False).iloc[0]
top5_bat  = batting_df.sort_values("runs", ascending=False).head(5)
top5_bowl = bowling_df.sort_values("wickets", ascending=False).head(5)
best_team = team_df.sort_values("win_percentage", ascending=False).iloc[0]

total_matches = len(matches_df)
total_teams   = team_df["team"].nunique()
total_runs    = int(team_df["runs_scored"].sum())
total_players = batting_df["batter"].nunique()
total_wickets = int(bowling_df["wickets"].sum())
total_sixes   = int(batting_df["sixes"].sum())

def initials(name):
    parts = name.split()
    return (parts[0][0] + parts[-1][0]).upper() if len(parts) > 1 else name[:2].upper()

# ─────────────────────────────────────────────
# ① OVERVIEW
# ─────────────────────────────────────────────
if page == "Overview":

    # Hero
    st.markdown(f"""
    <div class="hero-wrap">
        <div class="hero-eyebrow">IPL 2026 Season</div>
        <div class="hero-title">IPL <span>2026</span> Cricket Analytics Platform</div>
        <div class="hero-sub">Data. Insights. Predictions. A Deeper Game.</div>
        <div class="hero-tags">
            <span class="hero-tag">Player Stats</span>
            <span class="hero-tag">Team Analysis</span>
            <span class="hero-tag">Match Predictions</span>
            <span class="hero-tag">Data Explorer</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # KPI strip
    st.markdown(f"""
    <div class="kpi-strip">
        <div class="kpi-item">
            <div class="kpi-num">{total_matches}</div>
            <div class="kpi-lbl">Matches</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-num">{total_teams}</div>
            <div class="kpi-lbl">Teams</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-num">{total_runs:,}</div>
            <div class="kpi-lbl">Total Runs</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-num">{total_players}</div>
            <div class="kpi-lbl">Players</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-num">{total_wickets}</div>
            <div class="kpi-lbl">Wickets</div>
        </div>
        <div class="kpi-item">
            <div class="kpi-num">{total_sixes:,}</div>
            <div class="kpi-lbl">Sixes</div>
        </div>
        <div class="kpi-item" style="flex:1.5;">
            <div class="kpi-num" style="font-size:0.95rem;">{top_bat['batter']}</div>
            <div class="kpi-lbl">Orange Cap · {int(top_bat['runs'])} Runs</div>
        </div>
        <div class="kpi-item" style="flex:1.5;border-right:none;">
            <div class="kpi-num" style="font-size:0.95rem;">{top_bowl['bowler']}</div>
            <div class="kpi-lbl">Purple Cap · {int(top_bowl['wickets'])} Wkts</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Charts + Highlights
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    ch1, ch2, ch3 = st.columns([2, 2, 1.3])

    with ch1:
        st.markdown("#### Runs Scored by Team")
        fig = px.bar(
            team_df.sort_values("runs_scored"),
            x="runs_scored", y="team", orientation="h",
            color="runs_scored", color_continuous_scale=BLUE_SEQ, text="runs_scored"
        )
        fig.update_traces(texttemplate="%{text:,}", textposition="inside",
                          insidetextanchor="end", marker_line_width=0,
                          textfont=dict(color="white", size=11))
        fig.update_layout(**base_layout(height=340, coloraxis_showscale=False, title="",
                          xaxis=dict(range=[0, team_df["runs_scored"].max() * 1.15],
                                     automargin=True)))
        st.plotly_chart(fig, use_container_width=True)

    with ch2:
        st.markdown("#### Win % by Team")
        fig2 = px.bar(
            team_df.sort_values("win_percentage"),
            x="win_percentage", y="team", orientation="h",
            color="win_percentage", color_continuous_scale=BLUE_SEQ, text="win_percentage"
        )
        fig2.update_traces(texttemplate="%{text:.1f}%", textposition="inside",
                           insidetextanchor="end", marker_line_width=0,
                           textfont=dict(color="white", size=11))
        fig2.update_layout(**base_layout(height=340, coloraxis_showscale=False, title="",
                           xaxis=dict(range=[0, team_df["win_percentage"].max() * 1.15],
                                      automargin=True)))
        st.plotly_chart(fig2, use_container_width=True)

    with ch3:
        st.markdown("#### Season Highlights")
        st.markdown(f"""
        <div class="hl-card">
            <div class="hl-title">Champions</div>
            <div class="hl-val">{best_team['team'].replace('Royal Challengers Bengaluru','RCB').replace('Mumbai Indians','MI')}</div>
            <div class="hl-sub">{best_team['wins']}W &middot; {best_team['win_percentage']:.1f}%</div>
        </div>
        <div class="hl-card">
            <div class="hl-title">Orange Cap</div>
            <div class="hl-val">{top_bat['batter']}</div>
            <div class="hl-sub">{int(top_bat['runs'])} Runs &middot; SR {top_bat['strike_rate']:.1f}</div>
        </div>
        <div class="hl-card">
            <div class="hl-title">Purple Cap</div>
            <div class="hl-val">{top_bowl['bowler']}</div>
            <div class="hl-sub">{int(top_bowl['wickets'])} Wkts &middot; Eco {top_bowl['economy']:.2f}</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ② TEAM PERFORMANCE
# ─────────────────────────────────────────────
elif page == "Team Performance":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("Team Performance", "Wins, run rates, and head-to-head comparisons.", wrap=False)

    tab1, tab2, tab3 = st.tabs(["Season Overview", "Team Deep-Dive", "Head to Head"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(team_df.sort_values("wins", ascending=False),
                         x="team", y="wins", color="wins",
                         color_continuous_scale=BLUE_SEQ, text="wins", title="Wins by Team")
            fig.update_traces(textposition="outside", marker_line_width=0)
            fig.update_layout(**base_layout(height=360, xaxis_tickangle=-35, coloraxis_showscale=False))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.scatter(team_df, x="runs_scored", y="runs_conceded",
                              size="win_percentage", color="win_percentage",
                              hover_name="team", color_continuous_scale=BLUE_SEQ,
                              title="Runs Scored vs Conceded")
            fig2.update_layout(**base_layout(height=360))
            st.plotly_chart(fig2, use_container_width=True)

        sdf = team_df.sort_values("wins", ascending=False)
        fig3 = go.Figure()
        fig3.add_trace(go.Bar(name="Wins", x=sdf["team"], y=sdf["wins"],
                              marker_color=BLUE, text=sdf["wins"], textposition="outside"))
        fig3.add_trace(go.Bar(name="Losses", x=sdf["team"], y=sdf["losses"],
                              marker_color="#adb5bd", text=sdf["losses"], textposition="outside"))
        fig3.update_layout(**base_layout(barmode="group", height=340,
                                         title="Wins vs Losses", xaxis_tickangle=-35))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        sel = st.selectbox("Select a team", sorted(team_df["team"].unique()), key="td")
        row = team_df[team_df["team"] == sel].iloc[0]
        m1,m2,m3,m4,m5 = st.columns(5)
        m1.metric("Matches", int(row["matches_played"]))
        m2.metric("Wins",    int(row["wins"]))
        m3.metric("Losses",  int(row["losses"]))
        m4.metric("Win %",   f"{row['win_percentage']:.1f}%")
        m5.metric("Run Diff",f"{int(row['runs_scored']-row['runs_conceded']):+,}")

        c1, c2 = st.columns(2)
        with c1:
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=row["win_percentage"],
                title={"text": "Win %", "font": {"color": FONT_COL}},
                gauge={"axis": {"range": [0, 100], "tickcolor": FONT_COL, "tickfont": {"color": FONT_COL}},
                       "bar": {"color": BLUE}, "bgcolor": PLOT_BG, "borderwidth": 0,
                       "steps": [{"range": [0, 40],  "color": "#f8d7da"},
                                  {"range": [40, 65], "color": "#fff3cd"},
                                  {"range": [65, 100],"color": "#d1e7dd"}]},
                number={"suffix": "%", "font": {"color": BLUE, "size": 28}}))
            fig_g.update_layout(**base_layout(height=260))
            st.plotly_chart(fig_g, use_container_width=True)
        with c2:
            fig_rc = go.Figure()
            fig_rc.add_trace(go.Bar(x=["Runs Scored", "Runs Conceded"],
                                    y=[int(row["runs_scored"]), int(row["runs_conceded"])],
                                    marker_color=[BLUE, "#adb5bd"],
                                    text=[f"{int(row['runs_scored']):,}", f"{int(row['runs_conceded']):,}"],
                                    textposition="outside"))
            fig_rc.update_layout(**base_layout(height=260, title="Runs", showlegend=False))
            st.plotly_chart(fig_rc, use_container_width=True)

        team_phase = phase_df[phase_df["batting_team"] == sel]
        if not team_phase.empty:
            st.markdown("#### Phase-wise Performance")
            fig_ph = px.bar(team_phase, x="phase", y="runs", color="run_rate",
                            color_continuous_scale=BLUE_SEQ, text="runs",
                            title=f"{sel} — Runs by Phase")
            fig_ph.update_traces(textposition="outside", marker_line_width=0)
            fig_ph.update_layout(**base_layout(height=300, coloraxis_showscale=True))
            st.plotly_chart(fig_ph, use_container_width=True)

    with tab3:
        ca, cb = st.columns(2)
        with ca: t1 = st.selectbox("Team 1", sorted(team_df["team"].unique()), key="h1")
        with cb: t2 = st.selectbox("Team 2", sorted(team_df["team"].unique()), index=1, key="h2")
        if t1 == t2:
            st.warning("Select two different teams.")
        else:
            r1 = team_df[team_df["team"] == t1].iloc[0]
            r2 = team_df[team_df["team"] == t2].iloc[0]
            metrics = ["Matches", "Wins", "Losses", "Win %", "Runs Scored", "Runs Conceded"]
            v1 = [int(r1["matches_played"]), int(r1["wins"]), int(r1["losses"]),
                  round(r1["win_percentage"], 1), int(r1["runs_scored"]), int(r1["runs_conceded"])]
            v2 = [int(r2["matches_played"]), int(r2["wins"]), int(r2["losses"]),
                  round(r2["win_percentage"], 1), int(r2["runs_scored"]), int(r2["runs_conceded"])]
            fig = go.Figure()
            fig.add_trace(go.Bar(name=t1, x=metrics, y=v1, marker_color=BLUE, text=v1, textposition="outside"))
            fig.add_trace(go.Bar(name=t2, x=metrics, y=v2, marker_color=BLUE2, text=v2, textposition="outside"))
            fig.update_layout(**base_layout(barmode="group", height=400, title=f"{t1} vs {t2}"))
            st.plotly_chart(fig, use_container_width=True)
            winner = t1 if r1["win_percentage"] >= r2["win_percentage"] else t2
            insight(f"<b>{winner}</b> had the better season by win percentage.")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ③ PLAYER ANALYSIS
# ─────────────────────────────────────────────
elif page == "Player Analysis":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("Player Analysis", "Batting leaderboard, milestones, and player profiles.", wrap=False)

    tab1, tab2 = st.tabs(["Leaderboard", "Player Profile"])

    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1: min_b = st.slider("Min Balls Faced", 0, 500, 50, key="bmin")
        with c2: sort_col = st.selectbox("Sort By", ["runs", "strike_rate", "sixes", "fours", "boundary_percentage"], key="bsort")
        with c3: top_n = st.slider("Top N", 5, 30, 15, key="btopn")

        filt = batting_df[batting_df["balls_faced"] >= min_b].sort_values(sort_col, ascending=False).head(top_n)
        fig = px.bar(filt, x="batter", y=sort_col, color=sort_col,
                     color_continuous_scale=BLUE_SEQ, text=sort_col,
                     title=f"Top {top_n} by {sort_col.replace('_',' ').title()}")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", marker_line_width=0)
        fig.update_layout(**base_layout(height=380, xaxis_tickangle=-40, coloraxis_showscale=False))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            fig2 = px.scatter(filt, x="runs", y="strike_rate", hover_name="batter",
                              size="sixes", color="boundary_percentage",
                              color_continuous_scale=BLUE_SEQ, title="Runs vs Strike Rate")
            fig2.update_layout(**base_layout(height=340))
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            fig3 = px.scatter(filt, x="fours", y="sixes", hover_name="batter",
                              color="runs", color_continuous_scale=BLUE_SEQ, title="Fours vs Sixes")
            fig3.update_layout(**base_layout(height=340))
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("#### Full Batting Table")
        disp = batting_df.sort_values(sort_col, ascending=False)[
            ["batter", "runs", "balls_faced", "strike_rate", "fours", "sixes",
             "boundary_percentage", "dot_ball_percentage"]].reset_index(drop=True)
        disp.index += 1
        st.dataframe(disp, use_container_width=True, height=340)

    with tab2:
        sel_p = st.selectbox("Select a player", sorted(batting_df["batter"].unique()), key="pp")
        bat_row    = batting_df[batting_df["batter"] == sel_p].iloc[0]
        impact_row = player_impact_df[player_impact_df["batter"] == sel_p]
        has_bowl   = not impact_row.empty and not pd.isna(impact_row.iloc[0].get("wickets", float("nan")))
        has_bat    = int(bat_row.get("runs", 0)) > 50
        if has_bowl and has_bat:
            role = "All-Rounder"
        elif has_bowl:
            role = "Bowler"
        else:
            role = "Batter"

        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:1rem;margin-bottom:1rem;padding:1rem;
                    background:#ffffff;border-radius:12px;border:1px solid #dee2e6;'>
            <div style='width:52px;height:52px;border-radius:50%;background:#dbeafe;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1rem;font-weight:800;color:#1e40af;flex-shrink:0;'>
                {initials(sel_p)}</div>
            <div>
                <div style='font-size:1.3rem;font-weight:800;color:#2563eb;'>{sel_p}</div>
                <div style='font-size:0.78rem;color:#6c757d;text-transform:uppercase;
                            letter-spacing:1px;font-weight:700;'>{role}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        st.markdown("##### Batting")
        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Runs",        int(bat_row["runs"]))
        m2.metric("Balls",       int(bat_row["balls_faced"]))
        m3.metric("Strike Rate", f"{bat_row['strike_rate']:.1f}")
        m4.metric("4s",          int(bat_row["fours"]))
        m5.metric("6s",          int(bat_row["sixes"]))
        m6.metric("Boundary %",  f"{bat_row['boundary_percentage']:.1f}%")

        if not impact_row.empty:
            ir = impact_row.iloc[0]
            c1, c2 = st.columns(2)
            with c1:
                labels = ["Runs", "Strike Rate", "Avg Runs", "Boundary %", "50+ Scores", "Sixes"]
                vals   = [pct_rank(player_impact_df["runs"], ir.get("runs", 0)),
                          pct_rank(batting_df["strike_rate"], bat_row["strike_rate"]),
                          pct_rank(player_impact_df["average_runs"], ir.get("average_runs", 0)),
                          pct_rank(batting_df["boundary_percentage"], bat_row["boundary_percentage"]),
                          pct_rank(player_impact_df["scores_50_plus"], ir.get("scores_50_plus", 0)),
                          pct_rank(batting_df["sixes"], bat_row["sixes"])]
                fig_r = go.Figure(go.Scatterpolar(
                    r=vals + [vals[0]], theta=labels + [labels[0]],
                    fill="toself", line_color=BLUE, fillcolor="rgba(37,99,235,0.1)"))
                fig_r.update_layout(**base_layout(height=340, title="Batting Percentile Radar",
                    polar=dict(radialaxis=dict(visible=True, range=[0, 100],
                               tickfont=dict(color=FONT_COL), gridcolor=GRID_COL),
                               angularaxis=dict(tickfont=dict(color=FONT_COL), gridcolor=GRID_COL),
                               bgcolor=PLOT_BG)))
                st.plotly_chart(fig_r, use_container_width=True)
            with c2:
                ms = {"30+": ir.get("scores_30_plus", 0),
                      "50+": ir.get("scores_50_plus", 0),
                      "100+": ir.get("scores_100_plus", 0)}
                fig_m = go.Figure(go.Bar(
                    x=list(ms.keys()),
                    y=[v if pd.notna(v) else 0 for v in ms.values()],
                    marker_color=[BLUE, BLUE2, "#93c5fd"],
                    text=[v if pd.notna(v) else 0 for v in ms.values()],
                    textposition="outside"))
                fig_m.update_layout(**base_layout(height=340, title="Milestone Scores", showlegend=False))
                st.plotly_chart(fig_m, use_container_width=True)

        if has_bowl:
            st.divider()
            st.markdown("##### Bowling")
            pr = impact_row.iloc[0]
            b1, b2, b3, b4, b5, b6 = st.columns(6)
            b1.metric("Wickets",       int(pr["wickets"]))
            b2.metric("Matches",       int(pr["matches_bowled"]))
            b3.metric("Runs Conceded", int(pr["runs_conceded"]))
            b4.metric("Economy",       f"{pr['economy']:.2f}")
            avg = pr["bowling_average"]; sr = pr["bowling_strike_rate"]
            b5.metric("Avg",  f"{avg:.2f}" if np.isfinite(avg) else "—")
            b6.metric("SR",   f"{sr:.2f}"  if np.isfinite(sr)  else "—")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ④ BOWLING STATS
# ─────────────────────────────────────────────
elif page == "Bowling Stats":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("Bowling Stats", "Wickets, economy, hauls and dot ball analysis.", wrap=False)

    bowlers = player_impact_df[player_impact_df["wickets"].notna()].copy()
    tab1, tab2 = st.tabs(["Leaderboard", "Bowler Profile"])

    with tab1:
        c1, c2, c3 = st.columns(3)
        with c1: min_wk = st.slider("Min Wickets", 0, int(bowlers["wickets"].max()), 5, key="bwmin")
        with c2:
            bs = st.selectbox("Sort By", ["wickets", "economy", "bowling_average",
                                           "bowling_strike_rate", "bowling_dot_pct", "three_plus_wickets"], key="bwsort")
        with c3: top_nb = st.slider("Top N", 5, 30, 15, key="bwtopn")

        asc = bs in ["economy", "bowling_average", "bowling_strike_rate"]
        filtb = bowlers[bowlers["wickets"] >= min_wk].sort_values(bs, ascending=asc).head(top_nb)

        fig = px.bar(filtb, x="batter", y=bs, color=bs,
                     color_continuous_scale=BLUE_SEQ if not asc else BLUE_SEQ[::-1],
                     text=bs, title=f"Top {top_nb} by {bs.replace('_',' ').title()}")
        fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", marker_line_width=0)
        fig.update_layout(**base_layout(height=380, xaxis_tickangle=-40, coloraxis_showscale=False))
        st.plotly_chart(fig, use_container_width=True)

        c1, c2 = st.columns(2)
        with c1:
            valid = bowlers[(bowlers["wickets"] >= min_wk) & (bowlers["bowling_average"] < 200)]
            fig2  = px.scatter(valid, x="economy", y="wickets", hover_name="batter",
                               size="matches_bowled", color="bowling_dot_pct",
                               color_continuous_scale=BLUE_SEQ, title="Economy vs Wickets")
            fig2.update_layout(**base_layout(height=340))
            st.plotly_chart(fig2, use_container_width=True)
        with c2:
            hdf = bowlers[bowlers["wickets"] >= min_wk].sort_values("wickets", ascending=False).head(12)
            fig3 = go.Figure()
            fig3.add_trace(go.Bar(name="3W+", x=hdf["batter"], y=hdf["three_plus_wickets"], marker_color=BLUE))
            fig3.add_trace(go.Bar(name="4W+", x=hdf["batter"], y=hdf["four_plus_wickets"],  marker_color=BLUE2))
            fig3.add_trace(go.Bar(name="5W+", x=hdf["batter"], y=hdf["five_plus_wickets"],  marker_color="#93c5fd"))
            fig3.update_layout(**base_layout(barmode="group", height=340,
                                             xaxis_tickangle=-40, title="Wicket Hauls"))
            st.plotly_chart(fig3, use_container_width=True)

        st.markdown("#### Full Bowling Table")
        bd = bowlers[bowlers["wickets"] >= min_wk].sort_values(bs, ascending=asc)[
            ["batter", "matches_bowled", "wickets", "runs_conceded", "economy",
             "bowling_average", "bowling_strike_rate", "bowling_dot_pct",
             "three_plus_wickets", "best_match_wickets"]
        ].rename(columns={"batter": "player"}).reset_index(drop=True)
        bd.index += 1
        st.dataframe(bd, use_container_width=True, height=340)

    with tab2:
        sel_b = st.selectbox("Select Bowler", sorted(bowlers["batter"].unique()), key="bprofile")
        brow  = bowlers[bowlers["batter"] == sel_b].iloc[0]

        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:1rem;margin-bottom:1rem;padding:1rem;
                    background:#ffffff;border-radius:12px;border:1px solid #dee2e6;'>
            <div style='width:52px;height:52px;border-radius:50%;background:#dbeafe;
                        display:flex;align-items:center;justify-content:center;
                        font-size:1rem;font-weight:800;color:#1e40af;flex-shrink:0;'>
                {initials(sel_b)}</div>
            <div>
                <div style='font-size:1.3rem;font-weight:800;color:#2563eb;'>{sel_b}</div>
                <div style='font-size:0.78rem;color:#6c757d;text-transform:uppercase;
                            letter-spacing:1px;font-weight:700;'>Bowler Profile</div>
            </div>
        </div>""", unsafe_allow_html=True)

        m1, m2, m3, m4, m5, m6 = st.columns(6)
        m1.metric("Wickets",       int(brow["wickets"]))
        m2.metric("Matches",       int(brow["matches_bowled"]))
        m3.metric("Runs Conceded", int(brow["runs_conceded"]))
        m4.metric("Economy",       f"{brow['economy']:.2f}")
        avg = brow["bowling_average"]; sr = brow["bowling_strike_rate"]
        m5.metric("Avg", f"{avg:.2f}" if np.isfinite(avg) else "—")
        m6.metric("SR",  f"{sr:.2f}"  if np.isfinite(sr)  else "—")

        c1, c2 = st.columns(2)
        with c1:
            eco_val = float(brow["economy"])
            eco_max = max(20, round(eco_val + 3))
            fig_g = go.Figure(go.Indicator(
                mode="gauge+number", value=eco_val,
                title={"text": "Economy Rate", "font": {"color": FONT_COL}},
                gauge={"axis": {"range": [0, eco_max], "tickcolor": FONT_COL, "tickfont": {"color": FONT_COL}},
                       "bar": {"color": BLUE}, "bgcolor": PLOT_BG, "borderwidth": 0,
                       "steps": [{"range": [0, eco_max * 0.44],  "color": "#d1e7dd"},
                                  {"range": [eco_max * 0.44, eco_max * 0.63], "color": "#fff3cd"},
                                  {"range": [eco_max * 0.63, eco_max], "color": "#f8d7da"}]},
                number={"font": {"color": BLUE, "size": 28}}))
            fig_g.update_layout(**base_layout(height=260))
            st.plotly_chart(fig_g, use_container_width=True)
        with c2:
            haul_d = {"3W+": int(brow["three_plus_wickets"]),
                      "4W+": int(brow["four_plus_wickets"]),
                      "5W+": int(brow["five_plus_wickets"])}
            y_max = max(max(haul_d.values()) + 1, 3)
            fig_h = go.Figure(go.Bar(
                x=list(haul_d.keys()), y=list(haul_d.values()),
                marker_color=[BLUE, BLUE2, "#93c5fd"],
                text=list(haul_d.values()), textposition="outside"))
            fig_h.update_layout(**base_layout(height=260, title="Wicket Hauls", showlegend=False,
                                              yaxis=dict(range=[0, y_max])))
            st.plotly_chart(fig_h, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⑤ VENUE ANALYSIS
# ─────────────────────────────────────────────
elif page == "Venue Analysis":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("Venue Analysis", "Ground-by-ground scoring patterns and chase records.", wrap=False)

    tab1, tab2 = st.tabs(["All Venues", "Venue Deep-Dive"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.bar(venue_df.sort_values("average_match_runs", ascending=False),
                         x="venue", y="average_match_runs", color="average_match_runs",
                         color_continuous_scale=BLUE_SEQ, text="average_match_runs",
                         title="Avg Match Runs by Venue")
            fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", marker_line_width=0)
            fig.update_layout(**base_layout(height=380, xaxis_tickangle=-40, coloraxis_showscale=False))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            fig2 = px.scatter(venue_df, x="average_first_innings_score", y="chase_success_percentage",
                              size="matches_played", hover_name="venue",
                              color="chase_success_percentage", color_continuous_scale=BLUE_SEQ,
                              title="Avg 1st Innings vs Chase Success %")
            fig2.update_layout(**base_layout(height=380))
            st.plotly_chart(fig2, use_container_width=True)

    with tab2:
        sel_v = st.selectbox("Select Venue", sorted(venue_df["venue"].unique()), key="vsel")
        vrow  = venue_df[venue_df["venue"] == sel_v].iloc[0]
        v1, v2, v3, v4 = st.columns(4)
        v1.metric("Matches",         int(vrow["matches_played"]))
        v2.metric("Avg 1st Innings", f"{vrow['average_first_innings_score']:.1f}")
        v3.metric("Avg Match Runs",  f"{vrow['average_match_runs']:.1f}")
        v4.metric("Chase Success %", f"{vrow['chase_success_percentage']:.1f}%")

        c1, c2 = st.columns(2)
        with c1:
            fig_cv = go.Figure(go.Indicator(
                mode="gauge+number+delta", value=vrow["chase_success_percentage"],
                delta={"reference": venue_df["chase_success_percentage"].mean(), "valueformat": ".1f"},
                title={"text": "Chase Success %", "font": {"color": FONT_COL}},
                gauge={"axis": {"range": [0, 100], "tickcolor": FONT_COL, "tickfont": {"color": FONT_COL}},
                       "bar": {"color": BLUE}, "bgcolor": PLOT_BG, "borderwidth": 0,
                       "steps": [{"range": [0, 40],   "color": "#f8d7da"},
                                  {"range": [40, 65],  "color": "#fff3cd"},
                                  {"range": [65, 100], "color": "#d1e7dd"}]},
                number={"suffix": "%", "font": {"color": BLUE, "size": 24}}))
            fig_cv.update_layout(**base_layout(height=280))
            st.plotly_chart(fig_cv, use_container_width=True)
        with c2:
            summary = pd.DataFrame({
                "Metric": ["City", "Highest Score", "Chases Won", "Matches Defended"],
                "Value":  [str(vrow["city"]), str(int(vrow["highest_match_score"])),
                           str(int(vrow["chases_won"])), str(int(vrow["matches_defended"]))]})
            st.dataframe(summary, hide_index=True, use_container_width=True, height=200)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⑥ MATCH EXPLORER
# ─────────────────────────────────────────────
elif page == "Match Explorer":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("Match Explorer", "Drill into any match — innings scores, margins and results.", wrap=False)

    tab1, tab2 = st.tabs(["All Matches", "Match Details"])

    with tab1:
        c1, c2 = st.columns(2)
        with c1:
            fig = px.histogram(match_df, x="total_match_runs", nbins=20,
                               color_discrete_sequence=[BLUE], title="Distribution of Match Runs")
            fig.update_layout(**base_layout(height=320))
            st.plotly_chart(fig, use_container_width=True)
        with c2:
            res = match_df["result_type"].value_counts().reset_index()
            res.columns = ["Result", "Count"]
            fig2 = px.pie(res, names="Result", values="Count", hole=0.55,
                          color_discrete_sequence=[BLUE, BLUE2, "#93c5fd"],
                          title="Match Results")
            fig2.update_layout(**base_layout(height=320))
            fig2.update_traces(textinfo="label+percent", textfont=dict(color=FONT_COL))
            st.plotly_chart(fig2, use_container_width=True)

        top_m = match_df.sort_values("total_match_runs", ascending=False).head(10).copy()
        top_m["label"] = top_m["team1"] + " vs " + top_m["team2"]
        fig3 = px.bar(top_m, x="label", y="total_match_runs", color="total_match_runs",
                      color_continuous_scale=BLUE_SEQ, text="total_match_runs",
                      title="Top 10 Highest-Scoring Matches")
        fig3.update_traces(textposition="outside", marker_line_width=0)
        fig3.update_layout(**base_layout(height=360, xaxis_tickangle=-30, coloraxis_showscale=False))
        st.plotly_chart(fig3, use_container_width=True)

    with tab2:
        match_sorted = match_df.sort_values("match_id").reset_index(drop=True)
        match_sorted["match_num"] = match_sorted.index + 1
        opts = "Match " + match_sorted["match_num"].astype(str) + " — " + match_sorted["team1"] + " vs " + match_sorted["team2"]
        sel_m = st.selectbox("Select a Match", opts, key="msel")
        match_num = int(sel_m.split(" — ")[0].replace("Match ", ""))
        mrow = match_sorted[match_sorted["match_num"] == match_num].iloc[0]

        st.markdown(f"""
        <div style='display:flex;align-items:center;gap:0.8rem;margin-bottom:1rem;padding:1rem;
                    background:#ffffff;border-radius:12px;border:1px solid #dee2e6;'>
            <div>
                <div style='font-size:1.2rem;font-weight:800;color:#2563eb;'>
                    {mrow['team1']} <span style='color:#6c757d;font-size:0.9rem;'>vs</span> {mrow['team2']}
                </div>
                <div style='font-size:0.78rem;color:#6c757d;font-weight:600;'>{mrow['match_date']}</div>
            </div>
        </div>""", unsafe_allow_html=True)

        m1, m2, m3, m4 = st.columns(4)
        m1.metric("1st Innings", int(mrow["first_innings_runs"]))
        m2.metric("2nd Innings", int(mrow["second_innings_runs"]))
        m3.metric("Total Runs",  int(mrow["total_match_runs"]))
        m4.metric("Result",      mrow["result_type"])

        c1, c2 = st.columns(2)
        with c1:
            fig_i = go.Figure(go.Bar(
                x=["1st Innings", "2nd Innings"],
                y=[int(mrow["first_innings_runs"]), int(mrow["second_innings_runs"])],
                marker_color=[BLUE, BLUE2],
                text=[int(mrow["first_innings_runs"]), int(mrow["second_innings_runs"])],
                textposition="outside"))
            fig_i.update_layout(**base_layout(height=280, title="Innings Comparison", showlegend=False))
            st.plotly_chart(fig_i, use_container_width=True)
        with c2:
            det = pd.DataFrame({
                "Metric": ["Date", "1st Innings Team", "2nd Innings Team", "Winner", "Run Margin", "Wicket Margin"],
                "Value":  [str(mrow["match_date"]), str(mrow["first_innings_team"]),
                           str(mrow["second_innings_team"]), str(mrow["winner"]),
                           str(mrow["run_margin"]), str(mrow["wickets_margin"])]})
            st.dataframe(det, hide_index=True, use_container_width=True, height=240)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⑦ DATA EXPLORER
# ─────────────────────────────────────────────
elif page == "Data Explorer":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("IPL Data Explorer",
            "Select a question and get instant answers from IPL 2026 data.", wrap=False)

    team_names   = sorted(team_df["team"].dropna().unique())
    player_names = sorted(batting_df["batter"].dropna().unique())

    question_bank = {
        "Team Performance": [
            "How did the selected team perform in IPL 2026?",
            "How many matches did the selected team play?",
            "How many matches did the selected team win?",
            "What is the selected team's win percentage?",
            "How many runs did the selected team score?",
            "How many runs did the selected team concede?"],
        "Batting": [
            "Who scored the most runs?", "Who are the top 5 run scorers?",
            "Who hit the most sixes?", "Who hit the most fours?",
            "What was the selected player's strike rate?",
            "How many runs did the selected player score?"],
        "Bowling": [
            "Who took the most wickets?", "Who are the top 5 wicket takers?",
            "Who had the best economy rate?", "Who had the best bowling strike rate?",
            "What was the selected player's economy rate?",
            "How many wickets did the selected player take?"],
        "Phase Analysis": [
            "Which phase had the most runs?",
            "How did the selected team perform across phases?",
            "How did the selected team perform in the powerplay?",
            "How did the selected team perform in the middle overs?",
            "How did the selected team perform in the death overs?"],
        "Venue Analysis": [
            "Which venue had the highest average match score?",
            "Which venue had the highest match score?",
            "Which venue had the best chase success?"],
        "Match Analysis": [
            "Which was the highest-scoring match?",
            "How many matches were won by chasing?",
            "How many matches were defended?"],
        "Team Comparison": [
            "Which team had the highest win percentage?",
            "Which team scored the most runs?",
            "Which team conceded the most runs?",
            "Compare two teams"],
    }

    c1, c2 = st.columns(2)
    with c1: category   = st.selectbox("1. Category", list(question_bank.keys()), key="ai_cat")
    with c2: selected_q = st.selectbox("2. Question", question_bank[category], key="ai_q")

    sel_team_ai = sel_player_ai = cmp_t1 = cmp_t2 = None
    if category in ["Team Performance", "Phase Analysis"]:
        sel_team_ai = st.selectbox("Select Team", team_names, key="ai_team")
    if selected_q in ["What was the selected player's strike rate?",
                      "How many runs did the selected player score?",
                      "What was the selected player's economy rate?",
                      "How many wickets did the selected player take?"]:
        sel_player_ai = st.selectbox("Select Player", player_names, key="ai_player")
    if selected_q == "Compare two teams":
        cc1, cc2 = st.columns(2)
        with cc1: cmp_t1 = st.selectbox("Team 1", team_names, key="ai_ct1")
        with cc2: cmp_t2 = st.selectbox("Team 2", team_names, key="ai_ct2")

    if st.button("Generate Insight", key="ai_btn"):
        if category == "Team Performance":
            row = team_df[team_df["team"] == sel_team_ai].iloc[0]
            if "How did" in selected_q:
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Matches", int(row["matches_played"]))
                c2.metric("Wins",    int(row["wins"]))
                c3.metric("Losses",  int(row["losses"]))
                c4.metric("Win %",   f"{row['win_percentage']:.1f}%")
            elif "play?" in selected_q:
                st.info(f"**{sel_team_ai}** played **{int(row['matches_played'])}** matches.")
            elif "win?" in selected_q:
                st.info(f"**{sel_team_ai}** won **{int(row['wins'])}** matches.")
            elif "percentage" in selected_q:
                st.info(f"**{sel_team_ai}** win %: **{row['win_percentage']:.1f}%**")
            elif "score?" in selected_q:
                st.info(f"**{sel_team_ai}** scored **{int(row['runs_scored']):,}** runs.")
            elif "concede?" in selected_q:
                st.info(f"**{sel_team_ai}** conceded **{int(row['runs_conceded']):,}** runs.")

        elif category == "Batting":
            if "most runs" in selected_q or "top 5" in selected_q:
                res = batting_df.sort_values("runs", ascending=False).head(5)
                fig = px.bar(res, x="batter", y="runs", color="strike_rate",
                             color_continuous_scale=BLUE_SEQ, text="runs", title="Top 5 Run Scorers")
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=True))
                st.plotly_chart(fig, use_container_width=True)
                insight(f"<b>{res.iloc[0]['batter']}</b> led with <b>{int(res.iloc[0]['runs'])}</b> runs.")
            elif "sixes" in selected_q:
                res = batting_df.sort_values("sixes", ascending=False).head(5)
                fig = px.bar(res, x="batter", y="sixes", color="sixes",
                             color_continuous_scale=BLUE_SEQ, text="sixes", title="Most Sixes")
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False))
                st.plotly_chart(fig, use_container_width=True)
                insight(f"<b>{res.iloc[0]['batter']}</b> hit <b>{int(res.iloc[0]['sixes'])}</b> sixes.")
            elif "fours" in selected_q:
                res = batting_df.sort_values("fours", ascending=False).head(5)
                fig = px.bar(res, x="batter", y="fours", color="fours",
                             color_continuous_scale=BLUE_SEQ, text="fours", title="Most Fours")
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False))
                st.plotly_chart(fig, use_container_width=True)
                insight(f"<b>{res.iloc[0]['batter']}</b> hit <b>{int(res.iloc[0]['fours'])}</b> fours.")
            elif "strike rate" in selected_q:
                row = batting_df[batting_df["batter"] == sel_player_ai].iloc[0]
                st.info(f"**{sel_player_ai}** SR: **{row['strike_rate']:.2f}**")
            elif "runs did the" in selected_q:
                row = batting_df[batting_df["batter"] == sel_player_ai].iloc[0]
                st.info(f"**{sel_player_ai}** scored **{int(row['runs'])}** runs.")

        elif category == "Bowling":
            if "most wickets" in selected_q or "top 5" in selected_q:
                res = bowling_df.sort_values("wickets", ascending=False).head(5)
                fig = px.bar(res, x="bowler", y="wickets", color="economy",
                             color_continuous_scale=BLUE_SEQ, text="wickets", title="Top 5 Wicket Takers")
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=True))
                st.plotly_chart(fig, use_container_width=True)
                insight(f"<b>{res.iloc[0]['bowler']}</b> led with <b>{int(res.iloc[0]['wickets'])}</b> wickets.")
            elif "economy" in selected_q and "player" not in selected_q:
                res = bowling_df.sort_values("economy").head(5)
                fig = px.bar(res, x="bowler", y="economy", color="economy",
                             color_continuous_scale=BLUE_SEQ[::-1], text="economy", title="Best Economy Rates")
                fig.update_traces(texttemplate="%{text:.2f}", textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False))
                st.plotly_chart(fig, use_container_width=True)
            elif "strike rate" in selected_q and "player" not in selected_q:
                res = bowling_df.sort_values("bowling_strike_rate").head(5)
                fig = px.bar(res, x="bowler", y="bowling_strike_rate",
                             color="bowling_strike_rate", color_continuous_scale=BLUE_SEQ[::-1],
                             text="bowling_strike_rate", title="Best Bowling SR")
                fig.update_traces(texttemplate="%{text:.1f}", textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False))
                st.plotly_chart(fig, use_container_width=True)
            elif "economy" in selected_q and "player" in selected_q:
                row = bowling_df[bowling_df["bowler"] == sel_player_ai]
                if row.empty: st.warning(f"{sel_player_ai} has no bowling data.")
                else: st.info(f"**{sel_player_ai}** economy: **{row.iloc[0]['economy']:.2f}**")
            elif "wickets did" in selected_q:
                row = bowling_df[bowling_df["bowler"] == sel_player_ai]
                if row.empty: st.warning(f"{sel_player_ai} has no bowling data.")
                else: st.info(f"**{sel_player_ai}** took **{int(row.iloc[0]['wickets'])}** wickets.")

        elif category == "Phase Analysis":
            result = phase_df[phase_df["batting_team"] == sel_team_ai].copy()
            if "powerplay" in selected_q.lower():   result = result[result["phase"].str.lower() == "powerplay"]
            elif "middle" in selected_q.lower():    result = result[result["phase"].str.lower() == "middle"]
            elif "death" in selected_q.lower():     result = result[result["phase"].str.lower() == "death"]
            elif "most runs" in selected_q:         result = phase_df.groupby("phase", as_index=False)["runs"].sum()
            if not result.empty:
                fig = px.bar(result, x="phase", y="runs", color="runs",
                             color_continuous_scale=BLUE_SEQ, text="runs",
                             title=f"{sel_team_ai} — Phase Performance")
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False))
                st.plotly_chart(fig, use_container_width=True)

        elif category == "Venue Analysis":
            if "average" in selected_q:
                res = venue_df.sort_values("average_match_runs", ascending=False).head(5)
                fig = px.bar(res, x="venue", y="average_match_runs", color="average_match_runs",
                             color_continuous_scale=BLUE_SEQ, text="average_match_runs",
                             title="Highest Avg Match Scores")
                fig.update_traces(texttemplate="%{text:.0f}", textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False, xaxis_tickangle=-30))
                st.plotly_chart(fig, use_container_width=True)
                insight(f"<b>{res.iloc[0]['venue']}</b> avg: <b>{res.iloc[0]['average_match_runs']:.1f}</b> runs.")
            elif "highest match" in selected_q:
                res = venue_df.sort_values("highest_match_score", ascending=False).head(5)
                st.dataframe(res[["venue", "highest_match_score"]], hide_index=True, use_container_width=True)
            else:
                res = venue_df.sort_values("chase_success_percentage", ascending=False).head(5)
                fig = px.bar(res, x="venue", y="chase_success_percentage", color="chase_success_percentage",
                             color_continuous_scale=BLUE_SEQ, text="chase_success_percentage",
                             title="Best Chase Success %")
                fig.update_traces(texttemplate="%{text:.1f}%", textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False, xaxis_tickangle=-30))
                st.plotly_chart(fig, use_container_width=True)

        elif category == "Match Analysis":
            if "highest" in selected_q:
                res = match_df.sort_values("total_match_runs", ascending=False).head(5).copy()
                res["label"] = res["team1"] + " vs " + res["team2"]
                fig = px.bar(res, x="label", y="total_match_runs", color="total_match_runs",
                             color_continuous_scale=BLUE_SEQ, text="total_match_runs",
                             title="Highest Scoring Matches")
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False, xaxis_tickangle=-25))
                st.plotly_chart(fig, use_container_width=True)
            elif "chasing" in selected_q:
                st.info(f"**{int((match_df['result_type'] == 'Chased').sum())}** matches were won by chasing.")
            else:
                st.info(f"**{int((match_df['result_type'] == 'Defended').sum())}** matches were won by defending.")

        elif category == "Team Comparison":
            if selected_q == "Compare two teams":
                if cmp_t1 == cmp_t2:
                    st.warning("Select two different teams.")
                else:
                    a = team_df[team_df["team"] == cmp_t1].iloc[0]
                    b = team_df[team_df["team"] == cmp_t2].iloc[0]
                    metrics = ["Matches", "Wins", "Losses", "Win %", "Runs Scored", "Runs Conceded"]
                    v1 = [int(a["matches_played"]), int(a["wins"]), int(a["losses"]),
                          round(a["win_percentage"], 1), int(a["runs_scored"]), int(a["runs_conceded"])]
                    v2 = [int(b["matches_played"]), int(b["wins"]), int(b["losses"]),
                          round(b["win_percentage"], 1), int(b["runs_scored"]), int(b["runs_conceded"])]
                    fig = go.Figure()
                    fig.add_trace(go.Bar(name=cmp_t1, x=metrics, y=v1, marker_color=BLUE,  text=v1, textposition="outside"))
                    fig.add_trace(go.Bar(name=cmp_t2, x=metrics, y=v2, marker_color=BLUE2, text=v2, textposition="outside"))
                    fig.update_layout(**base_layout(barmode="group", height=400, title=f"{cmp_t1} vs {cmp_t2}"))
                    st.plotly_chart(fig, use_container_width=True)
                    winner = cmp_t1 if a["win_percentage"] >= b["win_percentage"] else cmp_t2
                    insight(f"<b>{winner}</b> had the better season by win percentage.")
            else:
                col = {"highest win": "win_percentage", "most runs": "runs_scored", "conceded": "runs_conceded"}
                key = next((v for k, v in col.items() if k in selected_q.lower()), "win_percentage")
                res = team_df.sort_values(key, ascending=False).head(5)
                fig = px.bar(res, x="team", y=key, color=key,
                             color_continuous_scale=BLUE_SEQ, text=key, title=selected_q)
                fig.update_traces(textposition="outside", marker_line_width=0)
                fig.update_layout(**base_layout(height=340, coloraxis_showscale=False))
                st.plotly_chart(fig, use_container_width=True)
                insight(f"<b>{res.iloc[0]['team']}</b> leads this category.")

        st.caption("Results computed directly from IPL 2026 match data.")

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# ⑧ MATCH PREDICTION
# ─────────────────────────────────────────────
elif page == "Match Prediction":
    st.markdown('<div class="sec-wrap">', unsafe_allow_html=True)
    section("ML Match Prediction",
            "Predict the winner using the trained Random Forest model.", wrap=False)

    c1, c2 = st.columns(2)
    with c1: pred_t1 = st.selectbox("Team 1", sorted(team_df["team"].unique()), key="pt1")
    with c2: pred_t2 = st.selectbox("Team 2", sorted(team_df["team"].unique()), index=1, key="pt2")

    if pred_t1 == pred_t2:
        st.warning("Please select two different teams.")
    else:
        if st.button("Predict Winner", key="pred_btn"):
            with st.spinner("Running model..."):
                r1 = team_df[team_df["team"] == pred_t1].iloc[0]
                r2 = team_df[team_df["team"] == pred_t2].iloc[0]
                inp = pd.DataFrame([{
                    "team1": pred_t1, "team2": pred_t2, "venue": "Narendra Modi Stadium",
                    "team1_prev_win_pct":   r1["win_percentage"],
                    "team2_prev_win_pct":   r2["win_percentage"],
                    "team1_recent_form":    r1["win_percentage"],
                    "team2_recent_form":    r2["win_percentage"],
                    "team1_avg_runs":       r1["runs_scored"]   / r1["matches_played"],
                    "team2_avg_runs":       r2["runs_scored"]   / r2["matches_played"],
                    "team1_avg_conceded":   r1["runs_conceded"] / r1["matches_played"],
                    "team2_avg_conceded":   r2["runs_conceded"] / r2["matches_played"],
                    "toss_winner_is_team1": 0, "toss_decision": "field"}])
                pred  = model.predict(inp)[0]
                probs = model.predict_proba(inp)[0]
                winner = pred_t1 if pred == 1 else pred_t2
                t1_pct = probs[1] * 100
                t2_pct = probs[0] * 100

            st.markdown(f"""
            <div style='background:#ffffff;border:1px solid #dee2e6;border-radius:12px;
                        padding:1.5rem 2rem;margin:1rem 0;text-align:center;'>
                <div style='font-size:0.85rem;color:#6c757d;font-weight:700;
                            text-transform:uppercase;letter-spacing:1px;margin-bottom:6px;'>Predicted Winner</div>
                <div style='font-size:2rem;font-weight:800;color:#2563eb;'>{winner}</div>
            </div>""", unsafe_allow_html=True)

            c1, c2 = st.columns(2)
            for col, team, pct, color in [(c1, pred_t1, t1_pct, BLUE), (c2, pred_t2, t2_pct, BLUE2)]:
                with col:
                    fig_g = go.Figure(go.Indicator(
                        mode="gauge+number", value=pct,
                        title={"text": team, "font": {"color": FONT_COL, "size": 13}},
                        gauge={"axis": {"range": [0, 100], "tickcolor": FONT_COL, "tickfont": {"color": FONT_COL}},
                               "bar": {"color": color}, "bgcolor": PLOT_BG, "borderwidth": 0,
                               "steps": [{"range": [0, 50],   "color": "#f8d7da"},
                                          {"range": [50, 100], "color": "#d1e7dd"}]},
                        number={"suffix": "%", "font": {"color": color, "size": 26}}))
                    fig_g.update_layout(**base_layout(height=260))
                    st.plotly_chart(fig_g, use_container_width=True)

            fig_pb = go.Figure(go.Bar(
                x=[pred_t1, pred_t2], y=[t1_pct, t2_pct],
                marker_color=[BLUE, BLUE2],
                text=[f"{t1_pct:.1f}%", f"{t2_pct:.1f}%"],
                textposition="outside"))
            fig_pb.update_layout(**base_layout(height=280, title="Win Probability", showlegend=False,
                                               yaxis=dict(range=[0, 120])))
            st.plotly_chart(fig_pb, use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ─────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────
st.markdown("""
<div class="footer">
    <div style="margin-bottom:0.3rem;">
        <a href="#">Players</a> · <a href="#">Teams</a> · <a href="#">Venues</a> ·
        <a href="#">Data</a> · <a href="#">Stats</a> · <a href="#">Cricket</a>
    </div>
    More Than a League. A Billion Emotions. &nbsp;·&nbsp; Built for Cricket Fans
</div>
""", unsafe_allow_html=True)
