import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# Streamlit setup
st.set_page_config(page_title="💧 Smart Irrigation Dashboard", layout="wide")

st.title("💧 Smart Irrigation Dashboard")
st.markdown("### Real-time Soil Moisture & Pump Activity (Dark Mode)")

BACKEND_URL = "http://127.0.0.1:5001"

# Persistent session storage
if "data" not in st.session_state:
    st.session_state.data = []

placeholder = st.empty()
refresh_interval = st.sidebar.slider("Refresh every (sec)", 2, 15, 5)

# ✅ Custom dark Matplotlib style
plt.style.use("dark_background")

def set_dark_theme(ax):
    """Apply consistent dark theme style."""
    ax.set_facecolor("#0E1117")
    ax.figure.set_facecolor("#0E1117")
    ax.tick_params(colors="#FAFAFA", which="both")
    for spine in ax.spines.values():
        spine.set_color("#FAFAFA")
    ax.xaxis.label.set_color("#FAFAFA")
    ax.yaxis.label.set_color("#FAFAFA")
    ax.title.set_color("#FAFAFA")
    ax.grid(True, color="#333333", linestyle="--", linewidth=0.5)

while True:
    try:
        # Get live data
        status_resp = requests.get(f"{BACKEND_URL}/status")
        pump_status = status_resp.json().get("pump_status", "UNKNOWN")

        moist_resp = requests.get(f"{BACKEND_URL}/latest_moisture")
        moist_data = moist_resp.json()
        moisture = moist_data.get("moisture")
        timestamp = moist_data.get("timestamp")

        # Update data
        if moisture is not None and timestamp is not None:
            ts = pd.to_datetime(timestamp)
            st.session_state.data.append({
                "time": ts,
                "moisture": moisture,
                "pump": pump_status
            })

        df = pd.DataFrame(st.session_state.data)

        with placeholder.container():
            col1, col2 = st.columns([2, 1])

            with col1:
                st.subheader("📊 Live Moisture Graph (Dark Theme)")

                fig, ax = plt.subplots(figsize=(12, 7))

                # --- Dark theme setup
                set_dark_theme(ax)

                # --- Moisture line with glowing color
                ax.plot(df["time"], df["moisture"], color="#00BFFF", linewidth=2.5, marker="o", label="Moisture")

                # --- Pump ON/OFF indicators
                on_points = df[df["pump"] == "ON"]
                off_points = df[df["pump"] == "OFF"]
                ax.scatter(on_points["time"], on_points["moisture"], color="#00FF7F", s=45, label="Pump ON", zorder=5)
                ax.scatter(off_points["time"], off_points["moisture"], color="#FF4500", s=60, label="Pump OFF", zorder=5)

                # --- Labels and formatting
                ax.set_xlabel("Time (HH:MM)", fontsize=8)
                ax.set_ylabel("Soil Moisture Reading", fontsize=8)
                ax.set_title("Live Soil Moisture with Pump Activity", fontsize=6, weight="bold")

                ax.xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
                fig.autofmt_xdate(rotation=30)
                ax.legend(facecolor="#0E1117", edgecolor="#0E1117", labelcolor="#FAFAFA")

                st.pyplot(fig)

            with col2:
                st.metric("Current Moisture", f"{moisture:.0f}" if moisture else "--")
                st.metric("Pump Status", pump_status)

                if pump_status == "ON":
                    st.success("💡 Pump is currently **ON**")
                elif pump_status == "OFF":
                    st.info("💤 Pump is currently **OFF**")
                else:
                    st.warning("Pump status unknown")

            st.markdown("#### Recent Readings")
            st.dataframe(
                df.tail(10).sort_values(by="time", ascending=False),
                use_container_width=True
            )

        time.sleep(refresh_interval)

    except Exception as e:
        st.error(f"Error: {e}")
        time.sleep(5)
