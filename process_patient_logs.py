import requests
from collections import defaultdict
import json
import numpy as np

# 1. Fetch live metrics from your running Spring Boot backend
SERVER_URL = "http://localhost:8080/api/v1/assessment/sessions"

try:
    response = requests.get(SERVER_URL)
    response.raise_for_status()
    sessions = response.json()
except Exception as e:
    print(f"❌ Error communicating with Spring Boot Server: {e}")
    exit()

# 2. Group sessions by core Patient ID (stripping drawing type suffixes)
patient_vault = defaultdict(list)

for session in sessions:
    raw_id = session.get("patientId", "UNKNOWN_PATIENT")
    raw_data = session.get("rawKinematicData", "[]")
    
    # Extract clean patient name/id (e.g., "56_ALVI" from "56_ALVI_SPIRAL")
    parts = raw_id.split('_')
    if len(parts) >= 2:
        clean_patient_id = f"{parts[0]}_{parts[1]}"
        test_profile = parts[-1] # SPIRAL, SQUARE, or TRIANGLE
    else:
        clean_patient_id = raw_id
        test_profile = "UNKNOWN"
        
    try:
        points = json.loads(raw_data) if isinstance(raw_data, str) else raw_data
    except Exception:
        continue # Skip if JSON string inside the DB is broken
        
    patient_vault[clean_patient_id].append({
        "profile": test_profile,
        "points": points
    })

# 3. Compute metrics and generate the aggregate log summary
print("=" * 70)
print("             NEUROSKETCH CLINICAL MULTI-SESSION LOG REPORT           ")
print("=" * 70)

for patient, records in patient_vault.items():
    print(f"\n👤 PATIENT FILE: {patient}")
    print(f"└── Total Completed Tasks: {len(records)} test vectors logged")
    
    for record in records:
        profile = record["profile"]
        points = record["points"]
        
        if not points:
            print(f"    ├── [{profile}] Empty dataset row.")
            continue
            
        # Extract fields safely for statistical math summaries
        pressures = [p.get("pressure", 0.0) for p in points if "pressure" in p]
        dts = [p.get("dt", 0.0) for p in points if "dt" in p]
        velocities = [p.get("velocity", 0.0) for p in points if "velocity" in p]
        
        # Clinical Calculations
        mean_p = np.mean(pressures) if pressures else 0.0
        var_p = np.var(pressures) if pressures else 0.0
        total_time = sum(dts)
        
        # Calculate Motor Hesitation Percentage
        hesitation_points = 0
        for p in points:
            v = p.get("velocity", 0.0)
            pr = p.get("pressure", 0.0)
            if v < 1.0 and pr > 0.1: # Stylus resting with downforce
                hesitation_points += 1
        
        hes_pct = (hesitation_points / len(points)) * 100 if points else 0.0
        status_flag = "⚠️  RISK ALERT" if hes_pct > 30.0 else "✅  HEALTHY BASELINE"
        
        print(f"    ├── [{profile:8}] Metrics Profile:")
        print(f"    │   ├── Total Task Duration: {total_time:.3f} sec")
        print(f"    │   ├── Mean Kinematic Force: {mean_p:.4f} units (Var: {var_p:.5f})")
        print(f"    │   ├── Motor Planning Hesitation: {hes_pct:.2f}% of test runtime")
        print(f"    │   └── Diagnostic Threshold Status: {status_flag}")
        print(f"    │")
    print("─" * 60)