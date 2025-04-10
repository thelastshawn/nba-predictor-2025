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
    st.info("Use this tool to explore player and team performance, including rolling stats and head-to-head history.")

    # Load logs
    player_logs = pd.read_csv("player_logs.csv")
    team_logs = pd.read_csv("team_logs.csv")

    # Format date
    player_logs["GAME_DATE"] = pd.to_datetime(player_logs["GAME_DATE"])
    team_logs["GAME_DATE"] = pd.to_datetime(team_logs["GAME_DATE"])

    # Choose available team column dynamically
    team_col = None
    for col in ["TEAM_NAME", "TEAM_ABBREVIATION", "TEAM_ID"]:
        if col in player_logs.columns:
            team_col = col
            break

    if team_col is None:
        st.error("🛑 No recognizable team column found in player_logs.csv")
    else:
        # Create filters
        data_type = st.selectbox("Select Data Type", ["Player", "Team"])
        rolling_window = st.selectbox("Rolling Window (Games)", [5, 10, 20])

        if data_type == "Player":
            available_teams = sorted(player_logs[team_col].dropna().unique())
            selected_team = st.selectbox("Select Team", available_teams)

            filtered_players = player_logs[player_logs[team_col] == selected_team]["PLAYER_NAME"].dropna().unique()
            selected_player = st.selectbox("Select Player", sorted(filtered_players))

            filtered_logs = player_logs[
                (player_logs["PLAYER_NAME"] == selected_player)
            ].sort_values("GAME_DATE", ascending=False).head(rolling_window)

            st.subheader(f"Last {rolling_window} Games for {selected_player}")
            st.dataframe(filtered_logs[["GAME_DATE", "MATCHUP", "PTS", "REB", "AST", "PLUS_MINUS"]].reset_index(drop=True))

        else:
            available_teams = sorted(team_logs["TEAM_NAME"].dropna().unique())
            selected_team = st.selectbox("Select Team", available_teams)

            filtered_logs = team_logs[
                (team_logs["TEAM_NAME"] == selected_team)
            ].sort_values("GAME_DATE", ascending=False).head(rolling_window)

            st.subheader(f"Last {rolling_window} Games for {selected_team}")
            st.dataframe(filtered_logs[["GAME_DATE", "MATCHUP", "PTS", "REB", "AST", "PLUS_MINUS"]].reset_index(drop=True))



# --- AI Prompter ---
with ai_tab:
    st.header("Ask AI Anything About NBA Stats")
    user_input = st.text_input("Ask a question or type a prompt")
    if user_input:
        st.write("(Response placeholder: AI output will be shown here.)")
