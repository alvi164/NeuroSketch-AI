import json
import requests
import numpy as np
from scipy.signal import butter, filtfilt, find_peaks

def fetch_patient_sessions():
    """Queries the local Spring Boot enterprise endpoints to ingest stored diagnostic data."""
    url = "http://localhost:8080/api/v1/assessment/sessions"
    try:
        print("[DATABASE CONNECTED] Pulling patient sessions for feature extraction...")
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"[SUCCESS] Retracted {len(data)} session entries from the backend core.")
            return data
        print(f"[API ERROR] Status code: {response.status_code}")
        return []
    except Exception as e:
        print(f"[NETWORK ERROR] Failed connecting to backend server: {e}")
        return []

def lowpass_filter(data, cutoff=15.0, fs=200.0, order=2):
    """Removes high-frequency hardware digitizer noise to isolate pure physiological motion."""
    if len(data) <= 6:  
        return data
    try:
        nyq = 0.5 * fs
        normal_cutoff = cutoff / nyq
        # Guardrail against invalid cutoff ratios if fs calculations drop
        if normal_cutoff >= 1.0 or normal_cutoff <= 0:
            normal_cutoff = 0.99
        b, a = butter(order, normal_cutoff, btype='low', analog=False)
        return filtfilt(b, a, data, padlen=min(len(data)-1, 3))
    except Exception:
        return data  # Fallback gracefully to raw data if filtering fails

def extract_neurological_features(session):
    """Analyzes time-series kinematic arrays for biomarker tracking with noise filtering."""
    session_id = session.get("id")
    patient_id = session.get("patientId")
    raw_json_str = session.get("rawKinematicData")
    
    if not raw_json_str:
        return None
        
    try:
        data_points = json.loads(raw_json_str)
    except Exception:
        return None

    if len(data_points) < 15:
        return None
        
    pressures = np.array([pt.get("pressure", 0) for pt in data_points])
    velocities = np.array([pt.get("velocity", 0) for pt in data_points])
    dts = np.array([pt.get("dt", 0.005) for pt in data_points])
    
    avg_dt = np.mean(dts) if np.mean(dts) > 0 else 0.005
    fs = 1.0 / avg_dt
    
    cleaned_velocities = lowpass_filter(velocities, cutoff=12.0, fs=fs, order=2)
    
    # 1. Micro-Hesitations
    hesitation_threshold = 0.02 
    hesitations = np.sum(cleaned_velocities < hesitation_threshold)
    hesitation_ratio = (hesitations / len(cleaned_velocities)) * 100
    
    # 2. Tremor Frequency Tracking
    velocity_diffs = np.abs(np.diff(cleaned_velocities))
    peaks, _ = find_peaks(velocity_diffs, prominence=0.001, distance=max(1, int(fs/20)))
    tremor_frequency = len(peaks) / max(0.1, np.sum(dts))
    
    if np.max(velocity_diffs) < 0.005:
        tremor_frequency = 0.0

    mean_pressure = np.mean(pressures)
    pressure_variance = np.var(pressures)

    return {
        "id": session_id,
        "patient": patient_id,
        "hesitation_percentage": round(hesitation_ratio, 2),
        "estimated_oscillation_hz": round(tremor_frequency, 2),
        "mean_pressure": round(mean_pressure, 4),
        "pressure_variance": round(pressure_variance, 6)
    }

def run_diagnostic_suite():
    sessions = fetch_patient_sessions()
    if not sessions:
        print("[ANALYTICS FAILURE] No active patient rows found inside the database schema.")
        return
        
    print("\n" + "="*60)
    print("      NEUROSKETCH AI - KINEMATIC DIAGNOSTIC METRICS REPORT")
    print("="*60)
    
    for session in sessions:
        report = extract_neurological_features(session)
        if report:
            print(f"\n[Session ID: {report['id']}] - Profile: {report['patient']}")
            print(f" └── Motor Planning Hesitations: {report['hesitation_percentage']}% of duration")
            print(f" └── Kinetic Tremor Footprint  : {report['estimated_oscillation_hz']} Hz Frequency Component")
            print(f" └── Mean Stylus Pressure      : {report['mean_pressure']} units (Variance: {report['pressure_variance']})")
            
            if 4.0 <= report['estimated_oscillation_hz'] <= 6.5:
                print(" ⚠️  [SCREENING FLAG] Velocity cadence aligns with rest/action tremor ranges (4-6Hz). Follow-up advised.")
            elif report['hesitation_percentage'] > 25.0:
                print(" ⚠️  [SCREENING FLAG] High bradykinesia index/micro-hesitation ratio detected.")
            else:
                print(" ✅  [SCREENING SUCCESS] Kinematic continuity falls within standard healthy baseline limits.")
    print("\n" + "="*60)

if __name__ == "__main__":
    run_diagnostic_suite()