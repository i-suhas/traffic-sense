import matplotlib.pyplot as plt
import streamlit as st

def calculate_signal_durations(traffic_data, emergency_road=None):
    """Calculate signal durations, prioritizing emergency vehicles and ensuring non-negative timings."""
    total_traffic = sum(traffic_data.values()) or 1  # Avoid division by zero
    signal_durations = {road: (traffic / total_traffic) * 120 for road, traffic in traffic_data.items()}

    if emergency_road:
        st.warning(f"🚨 Emergency detected on road {emergency_road}! Prioritizing this lane.")
        for road in signal_durations:
            if road == emergency_road:
                signal_durations[road] += 30  # Increase time for emergency lane
            else:
                signal_durations[road] = max(10, signal_durations[road] - 10)  # Ensure non-negative values

    return signal_durations

def visualize_traffic(traffic_data, signal_durations):
    """Visualize traffic data and signal durations using a pie chart and line graph."""
    roads = list(traffic_data.keys())
    traffic_values = list(traffic_data.values())
    durations = [signal_durations[road] for road in roads]

    # Pie Chart for Traffic Distribution
    fig1, ax1 = plt.subplots()
    ax1.pie(traffic_values, labels=roads, autopct='%1.1f%%', colors=['red', 'blue', 'green', 'orange'],
            startangle=90, wedgeprops={'edgecolor': 'black'})
    ax1.set_title("🚗 Traffic Distribution Across Roads")
    st.pyplot(fig1)

    # Line Graph for Signal Durations
    fig2, ax2 = plt.subplots()
    ax2.plot(roads, durations, marker='o', linestyle='-', color='green', label='Signal Duration')
    ax2.set_xlabel("Roads")
    ax2.set_ylabel("Signal Time (seconds)")
    ax2.set_title("⏳ Traffic Signal Durations")
    ax2.grid(True)
    ax2.legend()
    st.pyplot(fig2)
