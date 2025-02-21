import random

def detect_emergency_vehicle():
    """Simulate emergency vehicle detection with a 30% probability."""
    roads = ["A", "B", "C", "D"]
    return random.choice(roads)  # 30% chance of emergency
