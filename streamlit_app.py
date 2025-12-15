import streamlit as st
import pandas as pd
import numpy as np

# -----------------------------
# PAGE SETUP
# -----------------------------
st.set_page_config(
    page_title="Soccer Injury Prevention AI",
    layout="wide"
)

st.title("⚽ Soccer Injury Prediction & Prevention AI")
st.caption("Browser-only | Explainable | MLS-style monitoring")

# -----------------------------
# INJURY RISK ENGINE (NO ML)
# -----------------------------
def compute_injury_risk(
    acwr,
    fatigue_z,
    soreness_z,
    high_speed_distance,
    accelerations,
    decelerations
):
    risk = 0.0

    # ACWR contribution
    if acwr > 1.6:
        risk += 0.40
    elif acwr > 1.3:
        risk += 0.25
    elif acwr < 0.8:
        risk += 0.10

    # Wellness
    risk += max(0, fatigue_z) * 0.12
    risk += max(0, soreness_z) * 0.15

    # High-speed running
    if high_speed_distance > 1200:
        risk += 0.20
    elif high_speed_distance > 800:
        risk += 0.10

    # Accelerations / decelerations
    total_accel = accelerations + decelerations
    if total_accel > 140:
        risk += 0.15
    elif total_accel > 100:
        risk += 0.08

    return min(risk, 1.0)

# -----------------------------
# PREVENTION AGENT
# -----------------------------
def prevention_recommendation(risk):
    if risk >= 0.75:
        return "🚨 HIGH RISK: Medical screening + reduce load 40%"
    elif risk >= 0.55:
        return "⚠️ MODERATE RISK: Modify training, limit high-speed"
    elif risk >= 0.35:
        return "🟡 MONITOR: Emphasize recovery"
    else:
        return "🟢 LOW RISK: Full training allowed"

# -----------------------------
# SIDEBAR INPUT (STAFF VIEW)
# -----------------------------
st.sidebar.header("Player Daily Input")

acwr = st.sidebar.slider("ACWR", 0.5, 3.0, 1.15)
fatigue_z = st.sidebar.slider("Fatigue (Z-score)", -3.0, 3.0, 1.0)
soreness_z = st.sidebar.slider("Soreness (Z-score)", -3.0, 3.0, 0.8)

high_speed_distance = st.sidebar.number_input(
    "High-Speed Distance (m)", 0, 3000, 900
)

accelerations = st.sidebar.number_input(
    "Accelerations", 0, 150, 60
)

decelerations = st.sidebar.number_input(
    "Decelerations", 0, 150, 65
)

# -----------------------------
# RUN AGENT
# -----------------------------
risk = compute_injury_risk(
    acwr,
    fatigue_z,
    soreness_z,
    high_speed_distance,
    accelerations,
    decelerations
)

recommendation = prevention_recommendation(risk)

# -----------------------------
# DASHBOARD
# -----------------------------
col1, col2, col3 = st.columns(3)

col1.metric("Injury Risk", f"{risk * 100:.1f}%")
col2.metric("Risk Level", recommendation.split(":")[0])
col3.metric("Decision", "Train / Modify")

st.info(recommendation)

# -----------------------------
# EXPLAINABILITY
# -----------------------------
st.subheader("🧠 Risk Drivers")

drivers = []

if acwr > 1.3:
    drivers.append("📈 Acute workload spike (ACWR)")
if fatigue_z > 1:
    drivers.append("😴 Elevated fatigue")
if soreness_z > 1:
    drivers.append("🦵 Increased muscle soreness")
if high_speed_distance > 800:
    drivers.append("🏃 High-speed running exposure")
if accelerations + decelerations > 120:
    drivers.append("⚡ High neuromuscular load")

if drivers:
    for d in drivers:
        st.write(d)
else:
    st.write("✅ No major injury risk flags detected")

# -----------------------------
# WORKLOAD TREND (SIMULATED)
# -----------------------------
st.subheader("📊 28-Day Load Trend (Example)")

days = np.arange(28)
acute = np.random.normal(520, 70, 28)
chronic = np.linspace(480, 540, 28)

trend_df = pd.DataFrame({
    "Acute Load": acute,
    "Chronic Load": chronic
})

st.line_chart(trend_df)

# -----------------------------
# MEDICAL NOTES
# -----------------------------
st.subheader("📝 Medical Notes")
st.text_area(
    "Internal notes (demo only)",
    placeholder="Player reported hamstring tightness post-match..."
)

# -----------------------------
# FOOTER
# -----------------------------
st.caption(
    "Browser-only injury prevention system inspired by elite professional soccer."
)
