import streamlit as st
import pandas as pd
import json
from datetime import datetime

st.set_page_config(page_title="NBA AI Dashboard", layout="wide")
st.title("🏀 NBA Daily Prediction Dashboard")

# ---------- Tabs ----------
tabs = st.tabs(["Moneyline", "Spreads", "Totals (O/U)", "Player Props", "AI Prompter"])

# ---------- Tab 1: Moneyline ----------
with tabs[0]:
    st.header("💵 Moneyline Predictions")
    try:
        with open("today_predictions.json", "r") as f:
            moneyline_data = json.load(f)
        df_ml = pd.DataFrame(moneyline_data)
    except FileNotFoundError:
        st.error("❌ today_predictions.json not found.")
        df_ml = pd.DataFrame()

    if not df_ml.empty:
        df_ml["Predicted Win"] = df_ml["Predicted Win"].map({1: "✅ Win", 0: "❌ Loss"})
        df_ml["Confidence"] = df_ml["Confidence"].str.replace("%", "").astype(float)
        
        st.sidebar.subheader("🔍 Moneyline Filters")
        min_conf = st.sidebar.slider("Min Confidence %", 50.0, 100.0, 60.0)
        team_filter = st.sidebar.multiselect("Filter by Team", df_ml["Team"].unique(), default=df_ml["Team"].unique())

        df_filtered = df_ml[df_ml["Team"].isin(team_filter)]
        df_filtered = df_filtered[df_filtered["Confidence"] >= min_conf]

        st.dataframe(df_filtered.reset_index(drop=True), use_container_width=True)
        st.success(f"{len(df_filtered)} teams meet your filter criteria ✅")
    else:
        st.warning("No moneyline predictions available.")

# ---------- Tab 2: Spread Predictions ----------
with tabs[1]:
    st.header("📏 Spread Predictions")
    st.info("Coming soon! Upload `today_spreads.json` to activate this tab.")

# ---------- Tab 3: Totals (O/U) Predictions ----------
with tabs[2]:
    st.header("📊 Totals (Over/Under)")
    st.info("Coming soon! Upload `today_totals.json` to activate this tab.")

# ---------- Tab 4: Player Props ----------
with tabs[3]:
    st.header("🎯 Player Prop Predictions")
    st.info("Coming soon! Upload `today_props.json` to activate this tab.")

# ---------- Tab 5: AI Prompter ----------
with tabs[4]:
    st.header("🧠 AI Prompter")
    st.write("Use natural language to ask about NBA matchups, team stats, trends, etc.")
    prompt = st.text_area("Ask anything about NBA stats or games...")
    if st.button("Generate Insights"):
        st.info("💡 AI response feature coming soon.")
