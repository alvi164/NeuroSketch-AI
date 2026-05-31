
# NeuroSketch AI — Clinical Kinematic Assessment Framework

NeuroSketch AI is an advanced, quantitative kinematic telemetry framework designed for neuro-motor function screening and clinical handwriting analysis. Optimized specifically for high-resolution graphics tablets (such as the Huion HS611), the application records real-time drawing paths to extract clinical biomarkers, including velocity cadence, tremor signatures, and force distribution indices.

This platform bridges a high-performance Spring Boot data repository with an interactive PySide6 graphical interface to classify kinetic indicators associated with bradykinesia, rigidity, and motor micro-corrections.

## 💻 Project Architecture & Layout

The project is structured as a unified monorepo divided into a decoupled Spring Boot backend and a Python analytics pipeline:

```text
NeuroSketch AI/
├── neuro-backend/                  # Core Spring Boot REST API
│   ├── src/
│   │   └── main/
│   │       ├── java/
│   │       │   └── com/neurosketch/backend/
│   │       │       ├── BackendApplication.java
│   │       │       ├── controller/
│   │       │       │   └── SessionController.java
│   │       │       ├── model/
│   │       │       │   └── DrawingSession.java
│   │       │       └── repository/
│   │       │           └── DrawingSessionRepository.java
│   │       └── resources/
│   └── pom.xml
├── main_dashboard.py               # PySide6 Clinical Master Dashboard
├── neuro_analytics.py              # Signal Processing & Feature Extraction Engine
├── neuro_capture.py                # Digital Stylus Telemetry Capture Pipeline
├── neuro_visualizer.py             # Dual-Panel Signal Waveform Visualizer
└── process_patient_logs.py         # Log Preprocessing Utility

```

---

## 🚀 Key Features

* **3-Part Clinical Battery:** Standardized evaluation templates including **Spiral**, **Square**, and **Triangle** trace tasks.
* **Real-time Stylus Telemetry:** Captures absolute coordinates $(X, Y)$, high-fidelity stylus pressure tracking, and precise delta-time ($\Delta t$) intervals.
* **Advanced Signal Processing:** Integrates a second-order low-pass Butterworth filter ($12\text{ Hz}$ cutoff frequency) to isolate physiological tremors from mechanical noise.
* **Biomarker Quantitator:** Automatically calculates mean velocity, instantaneous acceleration, continuous jerk cost metrics, and dynamic hesitation thresholds.
* **Decoupled Local Engine:** Stores patient profiles and raw coordinate timelines securely via a managed local microservice framework.

---

## 🛠️ Tech Stack & Dependencies

### Backend Core

* **Language & Runtime:** Java 17
* **Framework:** Spring Boot 3.x
* **Database Integration:** Spring Data JPA + H2 Embedded Database
* **Build Automation:** Maven Wrapper (`mvnw`)

### Frontend Analytics

* **Language:** Python 3.10+
* **GUI Framework:** PySide6 (Qt for Python)
* **Data Processing:** NumPy, SciPy (Signal processing modules)
* **Data Visualization:** Matplotlib (Interactive UI multi-panel figures)

---

## ⚙️ Installation & Setup

### 1. Prerequisites

Ensure you have **Java 17 (JDK 17)** and **Python 3.10+** installed on your operating system and mapped to your system environmental variables (`PATH`).

### 2. Setting Up the Backend Core

Open your terminal window, navigate into the core directory, and boot the Spring Boot server instance using the automated wrapper file:

```cmd
cd "NeuroSketch AI/neuro-backend"
mvnw.cmd spring-boot:run

```

*Leave this terminal panel operational. The core service exposes its endpoints on local port `8080` once initial verification concludes.*

### 3. Setting Up the Frontend Dashboard

Open a secondary terminal panel to provision and trigger the desktop environment:

```bash
cd "NeuroSketch AI"
pip install -r requirements.txt
python main_dashboard.py

```

---

## 📊 Operational Guide

1. **Patient Registration:** Launch the `main_dashboard.py` window interface and provide a standardized clinical tracking file sequence inside the **Patient ID** prompt field.
2. **Assessment Execution:** Click **Start Full 3-Part Clinical Assessment**. The interface sequentially loads your specialized canvas tracking loops for the Spiral, Square, and Triangle executions.
3. **Biomarker Reporting:** Upon closing the target drawing window panels, the engine fetches data coordinates from the repository, prints calculated metric matrices directly inside the central logs interface, and pops up interactive dual-panel waveform charts.

---

## 🔬 Calibration Notes

The system utilizes adaptive metric filters customized to prevent false positive flags during deliberate drawing tasks:

* **Geometric Pauses:** Geometric thresholds adapt automatically to expect localized slowing events at the sharp corners of Square (**38%**) and Triangle (**42%**) executions.
* **Micro-Braking Corrections:** Uses a default `HESITATION_RATIO` value of **0.10** to filter target pen lifts and deliberate speed shifts safely.

---

## 👥 Credits & Framework

Developed under the **Syad Alvi Research Framework**.

* **Lead System Architect & Algorithm Development:** Syad Mehedi Hasan Alvi
* **Primary Repository Maintainer:** Alvi (`alvi164`)

```

```
