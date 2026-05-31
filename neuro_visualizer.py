import json
import requests
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import butter, filtfilt

def fetch_sessions():
    """Extracts the entire time-series repository from the Spring Boot enterprise core."""
    try:
        response = requests.get("http://localhost:8080/api/v1/assessment/sessions", timeout=5)
        return response.json() if response.status_code == 200 else []
    except Exception as e:
        print(f"[ERROR] Failed connecting to backend: {e}")
        return []

def lowpass_filter(data, cutoff=12.0, fs=200.0, order=2):
    """Filters out raw digitizer noise for exact motor baseline tracing."""
    if len(data) <= 6: return data
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    if normal_cutoff >= 1.0 or normal_cutoff <= 0: normal_cutoff = 0.99
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return filtfilt(b, a, data, padlen=min(len(data)-1, 3))

def visualize_patient_session(session_id):
    """Generates clinical-grade kinematic wave charts for a target assessment session."""
    sessions = fetch_sessions()
    session = next((s for s in sessions if s.get("id") == session_id), None)
    
    if not session or not session.get("rawKinematicData"):
        print(f"[ERROR] Session ID {session_id} not found or empty.")
        return

    # Parse JSON time-series arrays
    data_points = json.loads(session["rawKinematicData"])
    
    # Reconstruct timeline vectors
    dts = [pt.get("dt", 0.005) for pt in data_points]
    timestamps = np.cumsum(dts) - dts[0] # Convert intervals into a continuous seconds timeline
    pressures = np.array([pt.get("pressure", 0) for pt in data_points])
    velocities = np.array([pt.get("velocity", 0) for pt in data_points])
    
    # Calculate sampling frequency and apply low-pass filter
    fs = 1.0 / np.mean(dts) if np.mean(dts) > 0 else 200.0
    cleaned_velocities = lowpass_filter(velocities, cutoff=12.0, fs=fs)

    # Initialize the Medical Plot Layout
    plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    fig.suptitle(f"NeuroSketch AI - Clinical Kinematic Report\nPatient ID: {session['patientId']} | Session ID: {session_id}", fontsize=14, fontweight='bold', color='#2c3e50')

    # Plot 1: Stylus Pressure Tracking Over Time
    ax1.plot(timestamps, pressures, color='#e74c3c', linewidth=2, label='Raw Pressure Vector')
    ax1.set_ylabel("Stylus Pressure (0.0 - 1.0)", fontsize=11, fontweight='bold')
    ax1.set_title("Force Distribution Matrix", fontsize=11, color='#34495e')
    ax1.fill_between(timestamps, pressures, color='#e74c3c', alpha=0.1)
    ax1.legend(loc="upper right")

    # Plot 2: Velocity Processing Curve (Isolating Tremors & Hesitations)
    ax2.plot(timestamps, velocities, color='#bdc3c7', alpha=0.6, linestyle='--', label='Raw Digitizer Velocity')
    ax2.plot(timestamps, cleaned_velocities, color='#2bc0e4', linewidth=2, label='Physiological Component (Low-Pass)')
    ax2.set_xlabel("Time Elapsed (Seconds)", fontsize=11, fontweight='bold')
    ax2.set_ylabel("Velocity (Pixels/ms)", fontsize=11, fontweight='bold')
    ax2.set_title("Velocity Cadence & Acceleration Analysis", fontsize=11, color='#34495e')
    ax2.fill_between(timestamps, cleaned_velocities, color='#2bc0e4', alpha=0.15)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    print(f"[SUCCESS] Rendering graphical profile for Session #{session_id} on screen...")
    plt.show()

if __name__ == "__main__":
    # Let's inspect Session #14 (where your high bradykinesia hesitations were flagged)
    target_id = 14 
    visualize_patient_session(target_id)