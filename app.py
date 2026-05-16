import random
import time
from datetime import datetime

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title="Battery Monitoring System", layout="wide")

st.title("Live Battery Monitoring System")
st.subheader("Formula Student - Electronics Team")
st.caption("Demo mode: values are generated from simulated data.")

MAX_POINTS = 20

for key in ["voltage_data", "current_data", "temp_data", "time_data"]:
    if key not in st.session_state:
        st.session_state[key] = []


def generate_fake_data() -> dict:
    return {
        "voltage": round(random.uniform(12.0, 14.6), 2),
        "current": round(random.uniform(5.0, 120.0), 2),
        "temperature": round(random.uniform(24.0, 48.0), 1),
        "soc": random.randint(55, 100),
    }


def detect_faults(voltage: float, current: float, temperature: float) -> list[str]:
    faults = []

    if temperature > 45:
        faults.append("HIGH TEMPERATURE")
    if voltage < 11.5:
        faults.append("LOW VOLTAGE")
    if current > 100:
        faults.append("HIGH CURRENT")

    return faults if faults else ["NORMAL"]


readings = generate_fake_data()
voltage = readings["voltage"]
current = readings["current"]
temperature = readings["temperature"]
soc = readings["soc"]

faults = detect_faults(voltage=voltage, current=current, temperature=temperature)
is_normal = faults == ["NORMAL"]
current_time = datetime.now().strftime("%H:%M:%S")

st.session_state.voltage_data.append(voltage)
st.session_state.current_data.append(current)
st.session_state.temp_data.append(temperature)
st.session_state.time_data.append(current_time)

st.session_state.voltage_data = st.session_state.voltage_data[-MAX_POINTS:]
st.session_state.current_data = st.session_state.current_data[-MAX_POINTS:]
st.session_state.temp_data = st.session_state.temp_data[-MAX_POINTS:]
st.session_state.time_data = st.session_state.time_data[-MAX_POINTS:]

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("Voltage", f"{voltage} V")

with col2:
    st.metric("Current", f"{current} A")

with col3:
    st.metric("Temperature", f"{temperature} C")

with col4:
    st.metric("Battery", f"{soc}%")

st.subheader("Battery Charge")

if soc >= 60:
    gauge_color = "green"
elif soc >= 30:
    gauge_color = "orange"
else:
    gauge_color = "red"

fig_gauge = go.Figure(
    go.Indicator(
        mode="gauge+number",
        value=soc,
        title={"text": "SOC %"},
        gauge={
            "axis": {"range": [0, 100]},
            "bar": {"color": gauge_color},
        },
    )
)

st.plotly_chart(fig_gauge, use_container_width=True)

col5, col6 = st.columns(2)

with col5:
    st.subheader("Voltage History")
    voltage_df = pd.DataFrame(
        {
            "Time": st.session_state.time_data,
            "Voltage": st.session_state.voltage_data,
        }
    )
    st.line_chart(voltage_df.set_index("Time"))

with col6:
    st.subheader("Temperature History")
    temp_df = pd.DataFrame(
        {
            "Time": st.session_state.time_data,
            "Temperature": st.session_state.temp_data,
        }
    )
    st.line_chart(temp_df.set_index("Time"))

st.subheader("Current History")

current_df = pd.DataFrame(
    {
        "Time": st.session_state.time_data,
        "Current": st.session_state.current_data,
    }
)

st.line_chart(current_df.set_index("Time"))

st.subheader("System Status")

if is_normal:
    st.success("System Operating Normally")
else:
    for fault in faults:
        st.error(f"FAULT DETECTED: {fault}")

st.subheader("Battery Pack Information")

battery_info = {
    "Battery Type": "LiFePO4",
    "Cell Model": "Headway 38120HP",
    "Configuration": "4S10P",
    "Nominal Voltage": "12.8V",
    "Capacity": "40Ah",
    "BMS": "DALY Smart BMS",
    "Status": ", ".join(faults),
}

battery_df = pd.DataFrame(battery_info.items(), columns=["Parameter", "Value"])
st.table(battery_df)

time.sleep(1)
st.rerun()
