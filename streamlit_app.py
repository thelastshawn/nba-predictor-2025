import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="NBA Predictions", layout="wide")
st.title("🏀 TheLastShawn's NBA Daily Predictions")

# Tabs for views
tab1, tab2, tab3 = st.tabs(["💰 Moneyline", "📏 Spreads", "🎯 Player Props"])

# Load prediction data from cache
try:
    with open("cache.json", "r") as f:
        data = json.load(f)
    df = pd.DataFrame(data)
except FileNotFoundError:
    st.error("❌ cache.json not found. Run generate_predictions.py first.")
    st.stop()

# MONEYLINE TAB
with tab1:
    if not df.empty:
        df['Predicted Win'] = df['predicted_win'].map({1: "✅ Win", 0: "❌ Loss"})
        df['Confidence'] = df['confidence']
        df['Moneyline'] = df['moneyline']
        df['Implied Prob'] = df['implied_prob']
        df['Edge'] = df['edge']
        df = df[['team', 'Predicted Win', 'Confidence', 'Moneyline', 'Implied Prob', 'Edge']]

        st.sidebar.header("🔍 Filters")
        min_conf = st.sidebar.slider("Minimum Confidence %", 50.0, 100.0, 60.0)
        min_edge = st.sidebar.slider("Minimum Edge %", -20.0, 20.0, 0.0)
        team_filter = st.sidebar.multiselect("Filter by Team", df['team'].unique(), default=df['team'].unique())

        df_filtered = df[df['team'].isin(team_filter)]
        df_filtered = df_filtered[df_filtered['Confidence'].str.rstrip('%').astype(float) >= min_conf]
        df_filtered = df_filtered[df_filtered['Edge'].str.rstrip('%').astype(float) >= min_edge]

        st.markdown(f"### 🗓️ Predictions for {datetime.today().strftime('%B %d, %Y')}")
        st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
        st.success(f"{len(df_filtered)} teams meet your filter criteria ✅")

    else:
        st.warning("No prediction data available.")

# SPREADS TAB
with tab2:
    st.info("📏 Spread prediction model coming soon. This tab will show spread edges and recommended plays.")

# PLAYER PROPS TAB
with tab3:
    st.info("🎯 Player prop model coming soon. We'll show player points, rebounds, assists predictions and value bets.")
