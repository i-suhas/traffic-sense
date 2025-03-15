import streamlit as st
import time
import numpy as np  # For Kronecker delta function
from emergency_detector import detect_emergency_vehicle
from traffic_utils import calculate_signal_durations, visualize_traffic

def kronecker_delta(i, j):
    """Returns 1 if i == j, otherwise returns 0."""
    return np.kron([i == j], [1])[0]

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

def allocate_signal_times(signal_durations, emergency_road):
    """Allocate green signals dynamically based on congestion & emergency presence."""
    max_congestion_road = max(signal_durations, key=signal_durations.get)

    for road, duration in signal_durations.items():
        # Green light if it's the most congested road OR has emergency vehicle
        green_light = kronecker_delta(road, max_congestion_road) or kronecker_delta(road, emergency_road)
        
        if green_light:
            st.write(f"🚦 🟢 Green light for {road} - {int(duration)} seconds")
            time.sleep(duration / 10)  # Speed up for demo
        else:
            st.write(f"🔴 Red light for {road}")

def simulate_peak_hour_traffic():
    """Simulate peak hour traffic data."""
    st.sidebar.header("Peak Hour Traffic")
    roads = ['A', 'B', 'C', 'D']
    return {road: st.sidebar.slider(f"Peak hour traffic count for road {road}", 50, 1000, 500) for road in roads}



def simulate_low_traffic():
    """Simulate low traffic data."""
    st.sidebar.header("Low Traffic")
    roads = ['A', 'B', 'C', 'D']
    return {road: st.sidebar.slider(f"Low traffic count for road {road}", 0, 100, 50) for road in roads}

# Streamlit UI
st.title("🚦 Traffic Sense : A Smart Adaptive Signal system 🚨")
st.write("Optimize signals dynamically, handle emergency vehicles, and manage lanes efficiently.")
st.sidebar.header("🔧 Settings")
traffic_mode = st.sidebar.radio("Select Traffic Mode", ["Simulated Data", "Custom Input", "Peak Hour", "Low Traffic"])
enable_emergency = st.sidebar.checkbox("🚑 Enable Emergency Vehicle Detection", value=False)

# Select Traffic Mode
if traffic_mode == "Simulated Data":
    traffic_data = simulate_traffic_data()
elif traffic_mode == "Custom Input":
    traffic_data = get_custom_traffic_data()
elif traffic_mode == "Peak Hour":
    traffic_data = simulate_peak_hour_traffic()
else:
    traffic_data = simulate_low_traffic()

# Emergency Vehicle Handling
emergency_road = detect_emergency_vehicle() if enable_emergency else None

# Calculate Signal Durations Based on Traffic Density
signal_durations = calculate_signal_durations(traffic_data, emergency_road)

# Display Traffic Data & Signal Durations
st.subheader("🚗 Traffic Data")
st.write(traffic_data)
st.subheader("⏳ Signal Durations")
st.write(signal_durations)

# Visualize & Simulate Traffic Signal Allocation
visualize_traffic(traffic_data, signal_durations)
allocate_signal_times(signal_durations, emergency_road)
