Python 3.14.2 (v3.14.2:df793163d58, Dec  5 2025, 12:18:06) [Clang 16.0.0 (clang-1600.0.26.6)] on darwin
Enter "help" below or click "Help" above for more information.
import streamlit as st
import pandas as pd
import numpy as np

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="Professional Soccer Injury Prevention System",
    layout="wide"
)

# -------------------------------------------------
# HEADER (PITCH STYLE)
# -------------------------------------------------
st.title("⚽ Professional Soccer Injury Prevention System")
st.subheader("Reducing Soft-Tissue Injuries Through Load & Wellness Intelligence")

st.markdown("""
**Problem:**  
Soft-tissue injuries are one of the leading causes of missed matches, lost points,
and reduced player availability in professional soccer.

**Solution:**  
An AI-assisted decision system that combines:
- Training & match load
- Wellness monitoring
- Running & neuromuscular demands

to **predict injury risk and guide daily decisions**.
""")

st.divider()

# -------------------------------------------------
# INJURY RISK ENGINE (RULE-BASED, EXPLAINABLE)
# -------------------------------------------------
def compute_injury_risk(
    acwr,
    fatigue_z,
    soreness_z,
    high_speed_distance,
    accelerations,
    decelerations
):
    risk = 0.0

    # Load balance
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

    # Neuromuscular load
    if accelerations + decelerations > 140:
        risk += 0.15
    elif accelerations + decelerations > 100:
        risk += 0.08

    return min(risk, 1.0)

def prevention_recommendation(risk):
    if risk >= 0.75:
        return "🚨 HIGH RISK", "Medical screening + reduce training load 40%"
    elif risk >= 0.55:
        return "⚠️ MODERATE RISK", "Modified training, limit high-speed exposure"
    elif risk >= 0.35:
        return "🟡 MONITOR", "Maintain load, prioritize recovery strategies"
    else:
        return "🟢 LOW RISK", "Full training participation"

# -------------------------------------------------
# SIDEBAR — PLAYER INPUT (WHAT CLUBS ALREADY TRACK)
# -------------------------------------------------
st.sidebar.title("Daily Player Monitoring")

st.sidebar.caption("Inputs typically collected by MLS clubs")

acwr = st.sidebar.slider("ACWR (Acute : Chronic Load)", 0.5, 3.0, 1.15)
fatigue_z = st.sidebar.slider("Fatigue (Z-score)", -3.0, 3.0, 1.0)
soreness_z = st.sidebar.slider("Muscle Soreness (Z-score)", -3.0, 3.0, 0.8)

high_speed_distance = st.sidebar.number_input(
    "High-Speed Running (m)", 0, 3000, 950
)

accelerations = st.sidebar.number_input(
    "Accelerations", 0, 150, 60
)

decelerations = st.sidebar.number_input(
    "Decelerations", 0, 150, 65
)

# -------------------------------------------------
# RUN SYSTEM
# -------------------------------------------------
risk = compute_injury_risk(
    acwr,
    fatigue_z,
    soreness_z,
    high_speed_distance,
    accelerations,
    decelerations
)

status, action = prevention_recommendation(risk)

# -------------------------------------------------
# EXECUTIVE DASHBOARD VIEW
# -------------------------------------------------
st.subheader("📊 Daily Injury Risk Assessment")

col1, col2, col3 = st.columns(3)

col1.metric("Injury Risk Probability", f"{risk * 100:.1f}%")
col2.metric("Risk Classification", status)
col3.metric("Recommended Status", "Train / Modify")

st.success(f"**Recommended Action:** {action}")

# -------------------------------------------------
# TRUST & EXPLAINABILITY
# -------------------------------------------------
st.subheader("🧠 Why This Recommendation Was Made")

reasons = []

if acwr > 1.3:
    reasons.append("📈 Acute workload spike relative to chronic load")
if fatigue_z > 1:
    reasons.append("😴 Elevated fatigue reported by the player")
if soreness_z > 1:
    reasons.append("🦵 Increased muscle soreness")
if high_speed_distance > 800:
    reasons.append("🏃 High exposure to high-speed running")
if accelerations + decelerations > 120:
    reasons.append("⚡ High neuromuscular demand (accel/decel load)")

if reasons:
    for r in reasons:
        st.write(r)
else:
    st.write("✅ No major risk flags identified")

# -------------------------------------------------
# VISUAL STORYTELLING (FOR COACHES)
# -------------------------------------------------
st.subheader("📈 Load Trend Context (Last 28 Days – Example)")

days = np.arange(28)
acute_load = np.random.normal(520, 70, 28)
chronic_load = np.linspace(480, 540, 28)

trend_df = pd.DataFrame({
    "Acute Load": acute_load,
    "Chronic Load": chronic_load
})
... 
... st.line_chart(trend_df)
... 
... st.caption(
...     "Clubs use these trends to avoid sharp spikes that increase injury likelihood."
... )
... 
... # -------------------------------------------------
... # MEDICAL NOTES (DEMO SAFE)
... # -------------------------------------------------
... st.subheader("📝 Medical / Performance Staff Notes")
... 
... st.text_area(
...     "Internal notes (demo only)",
...     placeholder="Player reported hamstring tightness post-match. Monitoring advised."
... )
... 
... # -------------------------------------------------
... # CLOSING (PITCH)
... # -------------------------------------------------
... st.divider()
... 
... st.markdown("""
... ### 🚀 Value to the Club
... 
... - **Fewer soft-tissue injuries**
... - **Higher player availability**
... - **Better daily training decisions**
... - **Shared language between coaches & medical staff**
... 
... This system integrates seamlessly with existing GPS and wellness workflows
... used by professional soccer clubs.
... """)
... 
... st.caption(
...     "Demo version | Browser-only | AI-ready architecture"
... )
