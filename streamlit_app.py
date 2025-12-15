import streamlit as st
import pandas as pd
import numpy as np

# --------------------------------
# PAGE SETUP
# --------------------------------
st.set_page_config(
    page_title="Soccer Injury Prevention AI",
    layout="wide"
)

st.title("⚽ Soccer Injury Prediction & Prevention AI")
st.caption("Browser-only | MLS-style | Explainable Decision Support")

# --------------------------------
# CONFIG
# --------------------------------
N_PLAYERS = 25

# --------------------------------
# RISK ENGINE (RULE-BASED)
# --------------------------------
def compute_injury_risk(
    acwr,
    fatigue_z,
    soreness_z,
    high_speed_distance,
    accelerations,
    decelerations,
    match_congestion=False,
    return_to_play=False
):
    risk = 0.0

    # ACWR
    if acwr > 1.6:
        risk += 0.40
    elif acwr > 1.3:
        risk += 0.25
    elif acwr < 0.8:
        risk += 0.10

    # Wellness
    risk += max(0, fatigue_z) * 0.12
    risk += max(0, soreness_z) * 0.15

    # Running exposure
    if high_speed_distance > 1200:
        risk += 0.20
    elif high_speed_distance > 800:
        risk += 0.10

    if accelerations + decelerations > 140:
        risk += 0.15
    elif accelerations + decelerations > 100:
        risk += 0.08

    # Match congestion
    if match_congestion:
        risk += 0.15

    # Return-to-play protection
    if return_to_play:
        risk *= 1.25

    return min(risk, 1.0)

# --------------------------------
# PREVENTION AGENT
# --------------------------------
def prevention_recommendation(risk):
    if risk >= 0.75:
        return "🚨 HIGH RISK – Medical screening + reduce load 40%"
    elif risk >= 0.55:
        return "⚠️ MODERATE RISK – Modified training, limit HSR"
    elif risk >= 0.35:
        return "🟡 MONITOR – Recovery emphasis"
    else:
        return "🟢 LOW RISK – Full training allowed"

# --------------------------------
# SIDEBAR CONTROLS
# --------------------------------
st.sidebar.header("Global Settings")

match_congestion = st.sidebar.checkbox(
    "Match Congestion (2+ matches in 7 days)"
)

return_to_play_players = st.sidebar.multiselect(
    "Return-to-Play Players",
    [f"Player {i+1}" for i in range(N_PLAYERS)]
)

st.sidebar.markdown("---")
st.sidebar.header("Data Input")

uploaded_file = st.sidebar.file_uploader(
    "Upload Player CSV (optional)",
    type=["csv"]
)

# --------------------------------
# DATA SOURCE
# --------------------------------
@st.cache_data
def generate_squad():
    data = []
    for i in range(N_PLAYERS):
        data.append({
            "player": f"Player {i+1}",
            "acwr": np.random.uniform(0.7, 1.8),
            "fatigue_z": np.random.normal(0.5, 0.8),
            "soreness_z": np.random.normal(0.4, 0.7),
            "high_speed_distance": np.random.randint(400, 1400),
            "accelerations": np.random.randint(40, 90),
            "decelerations": np.random.randint(40, 90),
        })
    return pd.DataFrame(data)

if uploaded_file:
    squad_df = pd.read_csv(uploaded_file)
else:
    squad_df = generate_squad()

# --------------------------------
# APPLY AI AGENT TO SQUAD
# --------------------------------
risks = []
recommendations = []

for _, row in squad_df.iterrows():
    rtp = row["player"] in return_to_play_players

    risk = compute_injury_risk(
        row["acwr"],
        row["fatigue_z"],
        row["soreness_z"],
        row["high_speed_distance"],
        row["accelerations"],
        row["decelerations"],
        match_congestion,
        rtp
    )

    risks.append(risk)
    recommendations.append(prevention_recommendation(risk))

squad_df["risk"] = risks
squad_df["risk_pct"] = squad_df["risk"] * 100
squad_df["status"] = recommendations

# --------------------------------
# SQUAD DASHBOARD
# --------------------------------
st.subheader("🧑‍🤝‍🧑 Squad Injury Risk Overview")

def risk_color(val):
    if val >= 75:
        return "background-color:#ff4d4d"
    elif val >= 55:
        return "background-color:#ffa500"
    elif val >= 35:
        return "background-color:#fff3cd"
    else:
        return "background-color:#d4edda"

st.dataframe(
    squad_df[["player", "risk_pct", "status"]]
    .sort_values("risk_pct", ascending=False)
    .style.applymap(risk_color, subset=["risk_pct"]),
    use_container_width=True
)

# --------------------------------
# PLAYER DETAIL VIEW
# --------------------------------
st.subheader("🔍 Individual Player Detail")

selected_player = st.selectbox(
    "Select Player",
    squad_df["player"]
)

player_row = squad_df[squad_df.player == selected_player].iloc[0]

col1, col2, col3 = st.columns(3)
col1.metric("Risk", f"{player_row.risk_pct:.1f}%")
col2.metric("ACWR", f"{player_row.acwr:.2f}")
col3.metric("HSR (m)", int(player_row.high_speed_distance))

st.info(player_row.status)

# --------------------------------
# WORKLOAD TREND (SIMULATED)
# --------------------------------
st.subheader("📊 28-Day Workload Trend")

trend_df = pd.DataFrame({
    "Acute Load": np.random.normal(520, 60, 28),
    "Chronic Load": np.linspace(480, 540, 28)
})

st.line_chart(trend_df)

# --------------------------------
# ML UPGRADE NOTE
# --------------------------------
st.subheader("🧠 ML Upgrade Path")

st.markdown(
"""
This app is **ML-ready**.

To upgrade:
- Replace `compute_injury_risk()` with a trained model
- Keep the UI unchanged
- Deploy on a server that supports ML libraries

This mirrors how elite clubs productionize analytics.
"""
)

# --------------------------------
# FOOTER
# --------------------------------
st.caption(
    "Injury prevention decision-support system inspired by elite professional soccer."
)
