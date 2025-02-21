import streamlit as st
import time
from emergency_detector import detect_emergency_vehicle
from traffic_utils import calculate_signal_durations, visualize_traffic

def simulate_traffic_data():
    """Allow users to input traffic data using sliders."""
    st.sidebar.header("Adjust Traffic Counts")
    roads = ['A', 'B', 'C', 'D']
    return {road: st.sidebar.slider(f"Traffic count for road {road}", 10, 500, 50) for road in roads}

def get_custom_traffic_data():
    """Allow users to enter custom traffic data manually."""
    st.sidebar.header("Enter Custom Traffic Data")
    roads = ['A', 'B', 'C', 'D']
    return {road: st.sidebar.number_input(f"Traffic count for road {road}", min_value=10, max_value=1000, value=50) for road in roads}

def allocate_signal_times(signal_durations):
    for road, duration in signal_durations.items():
        st.write(f"🟢 Green light for road {road} - {int(duration)} seconds")
        time.sleep(duration / 10)  # Speed up for demo

# Streamlit UI
st.title("🚦 Traffic Sense : A Smart Adaptive Signal system 🚨")
st.write("Optimize signals dynamically, handle emergency vehicles, and manage lanes efficiently.")
st.sidebar.header("🔧 Settings")
traffic_mode = st.sidebar.radio("Select Traffic Mode", ["Simulated Data", "Custom Input"])
enable_emergency = st.sidebar.checkbox("🚑 Enable Emergency Vehicle Detection", value=False)

if traffic_mode == "Simulated Data":
    traffic_data = simulate_traffic_data()
else:
    traffic_data = get_custom_traffic_data()

emergency_road = detect_emergency_vehicle() if enable_emergency else None
signal_durations = calculate_signal_durations(traffic_data, emergency_road)

st.subheader("🚗 Traffic Data")
st.write(traffic_data)
st.subheader("⏳ Signal Durations")
st.write(signal_durations)

visualize_traffic(traffic_data, signal_durations)
allocate_signal_times(signal_durations)
