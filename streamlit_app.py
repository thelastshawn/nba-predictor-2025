import streamlit as st
import pandas as pd
import json

st.set_page_config(page_title="NBA Prediction Dashboard", layout="wide")
st.title("NBA Prediction Dashboard")

# Tabs
main_tab, spreads_tab, totals_tab, props_tab, research_tab, ai_tab = st.tabs([
    "Moneyline", "Spreads", "Totals", "Player Props", "Team/Player Research", "AI Prompter"])

# --- Moneyline Tab ---
with main_tab:
    st.header("Today's Moneyline Predictions")
    try:
        with open("today_predictions.json") as f:
            ml_data = json.load(f)
        ml_df = pd.DataFrame(ml_data)
        st.dataframe(ml_df)
    except Exception as e:
        st.warning(f"Moneyline predictions not available: {e}")

# --- Spreads Tab ---
with spreads_tab:
    st.header("Spread Predictions")
    try:
        uploaded_spread = st.file_uploader("Upload spread_predictions.json", type="json")
        if uploaded_spread:
            spread_data = json.load(uploaded_spread)
            spread_df = pd.DataFrame(spread_data)
            st.dataframe(spread_df)
    except Exception as e:
        st.warning(f"No spread predictions available: {e}")

# --- Totals Tab ---
with totals_tab:
    st.header("Over/Under Predictions")
    try:
        uploaded_totals = st.file_uploader("Upload totals_predictions.json", type="json")
        if uploaded_totals:
            totals_data = json.load(uploaded_totals)
            totals_df = pd.DataFrame(totals_data)
            st.dataframe(totals_df)
    except Exception as e:
        st.warning(f"No totals predictions available: {e}")

# --- Player Props Tab ---
with props_tab:
    st.header("Player Prop Predictions")
    try:
        uploaded_props = st.file_uploader("Upload props_predictions.json", type="json")
        if uploaded_props:
            props_data = json.load(uploaded_props)
            props_df = pd.DataFrame(props_data)
            st.dataframe(props_df)
    except Exception as e:
        st.warning(f"No player props available: {e}")

# --- Research Tab ---
with research_tab:
    st.header("Team/Player Rolling Averages & H2H Lookup")
    st.info("This section includes filters and stats for any team or player.")

    # Load cleaned logs
    player_logs = pd.read_csv("player_logs.csv")
    team_logs = pd.read_csv("team_logs.csv")

    tab_option = st.radio("Select Data Type", ["Player Research", "Team Research"])

    if tab_option == "Player Research":
        selected_player = st.selectbox("Choose Player", sorted(player_logs["PLAYER_NAME"].unique()))
        rolling_window = st.selectbox("Rolling Average (Games)", [5, 10, 20])
        player_df = player_logs[player_logs["PLAYER_NAME"] == selected_player].copy()
        player_df = player_df.sort_values("GAME_DATE")

        # Rolling stats
        player_df["PTS_avg"] = player_df["PTS"].rolling(rolling_window).mean()
        player_df["REB_avg"] = player_df["REB"].rolling(rolling_window).mean()
        player_df["AST_avg"] = player_df["AST"].rolling(rolling_window).mean()

        st.subheader(f"{selected_player} - Last {rolling_window} Games")
        st.dataframe(player_df[["GAME_DATE", "MATCHUP", "PTS", "REB", "AST", "PTS_avg", "REB_avg", "AST_avg"]].tail(20))

    elif tab_option == "Team Research":
        selected_team = st.selectbox("Choose Team", sorted(team_logs["TEAM_NAME"].unique()))
        rolling_window = st.selectbox("Rolling Average (Games)", [5, 10, 20])
        team_df = team_logs[team_logs["TEAM_NAME"] == selected_team].copy()
        team_df = team_df.sort_values("GAME_DATE")

        # Rolling stats
        team_df["PTS_avg"] = team_df["PTS"].rolling(rolling_window).mean()
        team_df["REB_avg"] = team_df["REB"].rolling(rolling_window).mean()
        team_df["AST_avg"] = team_df["AST"].rolling(rolling_window).mean()
        team_df["OPP_PTS_avg"] = team_df["OPP_PTS"].rolling(rolling_window).mean()

        st.subheader(f"{selected_team} - Last {rolling_window} Games")
        st.dataframe(team_df[["GAME_DATE", "MATCHUP", "PTS", "REB", "AST", "OPP_PTS", "PTS_avg", "REB_avg", "AST_avg", "OPP_PTS_avg"]].tail(20))

# --- AI Prompter ---
with ai_tab:
    st.header("Ask AI Anything About NBA Stats")
    user_input = st.text_input("Ask a question or type a prompt")
    if user_input:
        st.write("(Response placeholder: AI output will be shown here.)")
