import sys
import subprocess
import time
import requests
import json
import os
import numpy as np
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                               QPushButton, QLabel, QLineEdit, QTextEdit, QMessageBox, QFrame)
from PySide6.QtCore import QProcess, Qt
from PySide6.QtGui import QFont

class NeuroSketchMasterDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.backend_process = None
        self.start_backend_server()

    def initUI(self):
        self.setWindowTitle("NeuroSketch AI - Clinical Master Dashboard")
        self.setGeometry(100, 100, 850, 650)

        # Clinical Slate Theme Stylesheet
        self.setStyleSheet("""
            QWidget {
                background-color: #1e293b;
                color: #f8fafc;
                font-family: 'Segoe UI', Arial, sans-serif;
            }
            QLabel {
                font-size: 13px;
                font-weight: 600;
                color: #94a3b8;
            }
            QLineEdit {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
                color: #f8fafc;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #38bdf8;
            }
            QTextEdit {
                background-color: #0f172a;
                border: 1px solid #334155;
                border-radius: 6px;
                padding: 10px;
                color: #38bdf8;
                font-family: 'Consolas', monospace;
                font-size: 13px;
            }
            QPushButton {
                background-color: #0284c7;
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 15px;
                font-weight: bold;
                padding: 12px;
            }
            QPushButton:hover {
                background-color: #0369a1;
            }
            QPushButton:pressed {
                background-color: #075985;
            }
        """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 15)
        layout.setSpacing(15)

        # Header Title
        title_lbl = QLabel("NEUROSKETCH AI — CLINICAL BATTERY CONFIGURATOR")
        title_lbl.setStyleSheet("color: #38bdf8; font-size: 16px; font-weight: bold; letter-spacing: 1px;")
        layout.addWidget(title_lbl)

        # Centralized Patient Input Block
        input_layout = QHBoxLayout()
        self.patient_id_input = QLineEdit()
        self.patient_id_input.setPlaceholderText("Enter Patient ID (e.g., 2026_05_31_Alvi)")
        input_layout.addWidget(QLabel("Patient ID / Target File:"))
        input_layout.addWidget(self.patient_id_input)
        layout.addLayout(input_layout)

        # Unified Assessment Executon Button
        self.run_btn = QPushButton("🚀 START FULL 3-PART CLINICAL ASSESSMENT")
        self.run_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        self.run_btn.clicked.connect(self.execute_clinical_pipeline)
        layout.addWidget(self.run_btn)

        # Output Log Monitor Component
        self.console_output = QTextEdit()
        self.console_output.setReadOnly(True)
        self.console_output.setPlaceholderText("Real-time clinical metrics pipeline logging stream...")
        layout.addWidget(QLabel("Biomarker Analytics Engine Logs:"))
        layout.addWidget(self.console_output)

        # --- AUTHOR SEPARATOR AND ATTRIBUTION LABEL ---
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("background-color: #334155; max-height: 1px; border: none;")
        layout.addWidget(divider)

        author_label = QLabel("System Architecture & Algorithms Designed by: Syad Mehedi Hasan Alvi Research Framework")
        author_label.setStyleSheet("font-size: 11px; color: #64748b; font-weight: normal; font-style: italic;")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(author_label)
        # -----------------------------------------------

        self.setLayout(layout)

    def start_backend_server(self):
        self.console_output.append("⏳ Synchronizing with Spring Boot Core Data Framework...")
        try:
            self.backend_process = QProcess()

            # Properly indented and dynamically fetching path
            base_dir = os.path.dirname(os.path.abspath(__file__))
            project_working_dir = os.path.join(base_dir, "neuro-backend")
            self.backend_process.setWorkingDirectory(project_working_dir)

            # OS-agnostic command setup
            if os.name == 'nt':  # Windows
                self.backend_process.start("cmd.exe", ["/c", "mvn spring-boot:run"])
            else:  # Linux/macOS
                self.backend_process.start("mvn", ["spring-boot:run"])

            self.console_output.append("✅ Microservice Data Bridge established successfully.\n")
        except Exception as e:
            self.console_output.append(f"⚠️ Automated system boot bypassed: {str(e)}.")

    def execute_clinical_pipeline(self):
        patient_id = self.patient_id_input.text().strip()
        if not patient_id:
            QMessageBox.warning(self, "Validation Warning", "A valid Patient Profile Identifer is mandatory.")
            return

        self.console_output.clear()
        self.console_output.append(f"▶️ Initializing full dynamic diagnostic battery for: {patient_id}")

        shapes = ["SPIRAL", "SQUARE", "TRIANGLE"]

        for shape in shapes:
            self.console_output.append(f"\n🎨 Drawing Template Active: Launching {shape} task channel...")
            QApplication.processEvents()

            # Execute automated workflow loop via subprocess runtime links
            subprocess.run(["python", "neuro_capture.py", patient_id, shape], capture_output=True, text=True)
            self.console_output.append(f"✅ Data Stream captured and verified for {shape}.")
            QApplication.processEvents()
            time.sleep(0.4)

        self.console_output.append("\n📥 All profiles extracted. Fetching server database records...")
        QApplication.processEvents()
        self.fetch_and_analyze_all(patient_id)

    def fetch_and_analyze_all(self, patient_id):
        SERVER_URL = "http://localhost:8080/api/v1/assessment/sessions"
        try:
            response = requests.get(SERVER_URL, timeout=5)
            sessions = response.json()

            latest_runs = {"SPIRAL": None, "SQUARE": None, "TRIANGLE": None}
            for s in sessions:
                p_id = s.get("patientId", "")
                if patient_id in p_id:
                    if "SPIRAL" in p_id: latest_runs["SPIRAL"] = s
                    elif "SQUARE" in p_id: latest_runs["SQUARE"] = s
                    elif "TRIANGLE" in p_id: latest_runs["TRIANGLE"] = s

            all_chart_data = {}
            self.console_output.append("\n" + "="*50 + "\n          FINAL QUANTITATIVE BIOMARKER REPORT\n" + "="*50)

            for shape, session_data in latest_runs.items():
                if not session_data:
                    self.console_output.append(f"⚠️ Record Missing: Patient skipped or closed out {shape} task prematurely.")
                    continue

                raw_data = session_data.get("rawKinematicData", "[]")
                points = json.loads(raw_data) if isinstance(raw_data, str) else raw_data

                if not points:
                    continue

                pressures = [p.get("pressure", 0.0) for p in points]
                velocities = [p.get("velocity", 0.0) for p in points]
                dts = [p.get("dt", 0.0) for p in points]

                total_time = sum(dts)
                mean_p = np.mean(pressures) if pressures else 0

                # --- ADVANCED DYNAMIC HESITATION FILTER ---
                mean_v = np.mean(velocities) if velocities else 0
                dynamic_threshold = mean_v * 0.15 # Calibrates to device polling metrics

                hesitations = sum(1 for p in points if p.get("velocity", 0.0) < dynamic_threshold and p.get("pressure", 0.0) > 0.05)
                hes_pct = (hesitations / len(points)) * 100 if points else 0
                # ------------------------------------------

                status = "⚠️ RIGIDITY / BRADYKINESIA ALERT" if hes_pct > 22.0 else "✅ KINEMATIC CONTINUITY STABLE"

                self.console_output.append(f"\n[ {shape} KINETIC ANALYTICS ]")
                self.console_output.append(f"  └── Complete Assessment Window: {total_time:.3f} sec")
                self.console_output.append(f"  └── Integrated Stylus Load   : {mean_p:.4f} bar/units")
                self.console_output.append(f"  └── Dynamic Hesitation Index : {hes_pct:.2f}% -> {status}")

                all_chart_data[shape] = {
                    "time": total_time,
                    "velocities": velocities,
                    "pressures": pressures
                }

            self.console_output.append("\n📊 Generating high-fidelity visual analysis matrices...")
            self.render_diagnostic_plot(all_chart_data)

        except Exception as e:
            self.console_output.append(f"❌ Core API Link Interrupted: {str(e)}\nEnsure Spring Boot backend is active and accepts HTTP POST mappings.")

    def render_diagnostic_plot(self, all_chart_data):
        if not all_chart_data:
            return

        plt.style.use('dark_background')
        fig, axes = plt.subplots(len(all_chart_data), 1, figsize=(11, 8), sharex=False)
        fig.suptitle('NeuroSketch AI - Enterprise Multi-Panel Wave Analysis', fontsize=13, fontweight='bold', color='#38bdf8')

        if len(all_chart_data) == 1:
            axes = [axes]

        for ax, (shape, data) in zip(axes, all_chart_data.items()):
            time_axis = np.linspace(0, data["time"], len(data["velocities"]))

            ax.set_ylabel('Velocity (px/s)', color='#38bdf8', fontweight='bold')
            ax.plot(time_axis, data["velocities"], color='#0284c7', linewidth=2, label=f'{shape} Speed profile')
            ax.tick_params(axis='y', labelcolor='#38bdf8')
            ax.set_title(f"Evaluation Template Matrix: {shape}", color='#e2e8f0', pad=4, fontsize=11)
            ax.grid(True, color='#334155', alpha=0.5)

            ax2 = ax.twinx()
            ax2.set_ylabel('Pressure Applied', color='#f43f5e', fontweight='bold')
            ax2.plot(time_axis, data["pressures"], color='#f43f5e', linestyle='--', alpha=0.8, label='Force Curve')
            ax2.tick_params(axis='y', labelcolor='#f43f5e')

        plt.xlabel('Session Timeline (Seconds)', color='#94a3b8')
        fig.tight_layout()
        plt.show()

    def closeEvent(self, event):
        if self.backend_process and self.backend_process.state() == QProcess.ProcessState.Running:
            self.backend_process.terminate()
        event.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = NeuroSketchMasterDashboard()
    ex.show()
    sys.exit(app.exec())