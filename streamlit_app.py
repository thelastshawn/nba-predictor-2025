import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="NBA Predictions", layout="wide")
st.title("🏀 NBA AI Prediction Dashboard")

# Load prediction data from cache
try:
    with open("cache.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
except FileNotFoundError:
    st.error("❌ cache.json not found. Run generate_predictions.py first.")
    st.stop()

# Format columns if available
if not df.empty:
    df['Predicted Win'] = df['predicted_win'].map({1: "✅ Win", 0: "❌ Loss"})
    df['Confidence'] = df['confidence']
    df['Moneyline'] = df['moneyline']
    df['Implied Prob'] = df['implied_prob']
    df['Edge'] = df['edge']

# Sidebar Navigation
st.sidebar.title("📊 Navigation")
tab = st.sidebar.radio("Select a View", [
    "Moneyline Predictions",
    "Spread Predictions",
    "Totals O/U Predictions",
    "Player Prop Predictions",
    "Team & Player Research",
    "AI Prompter"
])

# Moneyline Tab
if tab == "Moneyline Predictions":
    if not df.empty:
        df_ml = df[['team', 'Predicted Win', 'Confidence', 'Moneyline', 'Implied Prob', 'Edge']]
        st.sidebar.header("🔍 Filters")
        min_conf = st.sidebar.slider("Minimum Confidence %", 50.0, 100.0, 60.0)
        min_edge = st.sidebar.slider("Minimum Edge %", -20.0, 20.0, 0.0)
        team_filter = st.sidebar.multiselect("Filter by Team", df_ml['team'].unique(), default=df_ml['team'].unique())

        df_filtered = df_ml[df_ml['team'].isin(team_filter)]
        df_filtered = df_filtered[df_filtered['Confidence'].str.rstrip('%').astype(float) >= min_conf]
        df_filtered = df_filtered[df_filtered['Edge'].str.rstrip('%').astype(float) >= min_edge]

        st.markdown(f"### 🗓️ Moneyline Predictions for {datetime.today().strftime('%B %d, %Y')}")
        st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)

# Spread Predictions Tab
elif tab == "Spread Predictions":
    st.markdown("### 📏 Spread Predictions")
    st.info("This section will show AI spread predictions. Integrate your spread_model.pkl + live spreads here.")

# Totals Predictions Tab
elif tab == "Totals O/U Predictions":
    st.markdown("### 📊 Over/Under Totals Predictions")
    st.info("This section will display AI total points predictions (O/U). Integrate totals_model.pkl and daily odds.")

# Player Props Tab
elif tab == "Player Prop Predictions":
    st.markdown("### 👤 Player Prop Predictions")
    st.warning("Coming soon! Will support points, assists, rebounds, etc.")

# Research Tool Tab
elif tab == "Team & Player Research":
    st.markdown("### 🔍 NBA Team & Player Research Tool")
    st.info("Use this to explore rolling 10-game stats, team matchups, and H2H data. Integrate pre-processed stats here.")

# AI Prompter Tab
elif tab == "AI Prompter":
    st.markdown("### 🤖 AI Assistant")
    st.text_area("Ask me anything about NBA stats, teams, or predictions:", placeholder="e.g. What’s the Lakers’ record vs Warriors in their last 10 meetings?")
    st.button("Submit", help="Coming soon: Add OpenAI/GPT response integration.")
st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
    st.success(f"{len(df_filtered)} teams meet your filter criteria ✅")

else:
    st.warning("No prediction data available.")
