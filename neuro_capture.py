import sys
import time
import math
import json
import requests
from PySide6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                               QPushButton, QLabel, QFrame, QSplitter, QSizePolicy)
from PySide6.QtGui import QPainter, QPen, QTabletEvent, QMouseEvent, QColor
from PySide6.QtCore import Qt, QPointF

class ShapeReferenceWidget(QFrame):
    """Generates an expanded geometric baseline template for real-time patient targeting."""
    def __init__(self, shape_type):
        super().__init__()
        self.shape_type = shape_type
        self.setStyleSheet("background-color: #1e293b; border: 2px solid #475569; border-radius: 6px;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        painter.setPen(QPen(QColor("#38bdf8"), 4, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap))
        cx, cy = self.width() // 2, self.height() // 2
        scale_factor = min(self.width(), self.height())

        if self.shape_type == "SPIRAL":
            points = []
            for theta in range(0, 1500, 4):
                rad = math.radians(theta)
                r = (scale_factor * 0.00028) * theta
                x = cx + r * math.cos(rad)
                y = cy + r * math.sin(rad)
                points.append(QPointF(x, y))
            for i in range(len(points) - 1):
                painter.drawLine(points[i], points[i+1])

        elif self.shape_type == "SQUARE":
            size = int(scale_factor * 0.72)
            painter.drawRect(cx - size//2, cy - size//2, size, size)

        elif self.shape_type == "TRIANGLE":
            size = scale_factor * 0.8
            h = size * math.sqrt(3) / 2
            p1 = QPointF(cx, cy - h/2)
            p2 = QPointF(cx - size/2, cy + h/2)
            p3 = QPointF(cx + size/2, cy + h/2)
            painter.drawPolygon([p1, p2, p3])


class IsolatedDrawingCanvas(QFrame):
    """Main drawing interface tracking real-time position, time, and stylus metrics."""
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: #0f172a; border: 3px solid #0284c7; border-radius: 6px;")
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

        self.drawing = False
        self.last_point = QPointF()
        self.last_time = 0
        self.lines = []
        self.kinematic_data = []

    def tabletEvent(self, event: QTabletEvent):
        pos = self.mapFromGlobal(event.globalPosition())
        if event.type() == QTabletEvent.Type.TabletPress:
            self.start_stroke(pos, event.pressure())
            event.accept()
        elif event.type() == QTabletEvent.Type.TabletMove:
            self.continue_stroke(pos, event.pressure())
            event.accept()
        elif event.type() == QTabletEvent.Type.TabletRelease:
            self.end_stroke()
            event.accept()

    def mousePressEvent(self, event: QMouseEvent):
        self.start_stroke(event.position(), 0.6)

    def mouseMoveEvent(self, event: QMouseEvent):
        if self.drawing:
            self.continue_stroke(event.position(), 0.6)

    def mouseReleaseEvent(self, event: QMouseEvent):
        if self.drawing:
            self.end_stroke()

    def start_stroke(self, pos, pressure):
        self.drawing = True
        self.last_point = pos
        self.last_time = time.time()
        self.record_point(pos.x(), pos.y(), pressure)

    def continue_stroke(self, pos, pressure):
        if not self.drawing:
            return

        if self.rect().contains(pos.toPoint()):
            self.lines.append((self.last_point, pos))
            self.update()

            current_time = time.time()
            dt = current_time - self.last_time
            dx = pos.x() - self.last_point.x()
            dy = pos.y() - self.last_point.y()

            velocity = math.sqrt(dx**2 + dy**2) / dt if dt > 0 else 0
            self.record_point(pos.x(), pos.y(), pressure, dt, velocity)

            self.last_point = pos
            self.last_time = current_time

    def end_stroke(self):
        self.drawing = False

    def record_point(self, x, y, pressure, dt=0.0, velocity=0.0):
        self.kinematic_data.append({
            "x": round(x, 2),
            "y": round(y, 2),
            "pressure": round(pressure, 4),
            "dt": round(dt, 4),
            "velocity": round(velocity, 4)
        })

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        pen = QPen(QColor("#34d399"), 3, Qt.PenStyle.SolidLine, Qt.PenCapStyle.RoundCap, Qt.PenJoinStyle.RoundJoin)
        painter.setPen(pen)
        for line in self.lines:
            painter.drawLine(line[0], line[1])


class NeuroCaptureApp(QMainWindow):
    def __init__(self, patient_id, shape_type):
        super().__init__()
        self.patient_id = patient_id
        self.shape_type = shape_type

        self.setWindowTitle(f"Clinical Capture Pad — Active Module: {self.shape_type}")

        main_central_widget = QWidget()
        main_central_widget.setStyleSheet("background-color: #0f172a;")
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(15, 15, 15, 10)
        main_layout.setSpacing(12)

        # Clinical Header Context Bar
        header = QLabel(f"🧬 PATIENT IDENTIFIER: {self.patient_id}    |    🎯 ASSIGNED TASK EVALUATION: {self.shape_type}")
        header.setStyleSheet("font-size: 13px; font-weight: bold; padding: 8px; background-color: #1e293b; border: 1px solid #334155; color: #cbd5e1; border-radius: 4px;")
        header.setMaximumHeight(40)
        main_layout.addWidget(header)

        # Space-Maximized Layout Splitter
        self.splitter = QSplitter(Qt.Orientation.Horizontal)
        self.splitter.setStyleSheet("QSplitter::handle { background-color: #334155; width: 4px; }")

        # Left Segment (Target Pattern Reference)
        left_container = QWidget()
        left_layout = QVBoxLayout(left_container)
        left_layout.setContentsMargins(0, 0, 0, 0)
        ref_label = QLabel("VISUAL EXAM TEMPLATE REFERENCE")
        ref_label.setStyleSheet("color: #94a3b8; font-size: 11px; font-weight: bold;")
        left_layout.addWidget(ref_label)
        self.reference_view = ShapeReferenceWidget(self.shape_type)
        left_layout.addWidget(self.reference_view, stretch=1)
        self.splitter.addWidget(left_container)

        # Right Segment (Isolated Spatial Capture Area)
        right_container = QWidget()
        right_layout = QVBoxLayout(right_container)
        right_layout.setContentsMargins(0, 0, 0, 0)
        draw_label = QLabel("PATIENT CAPTURE WORKSPACE ZONE")
        draw_label.setStyleSheet("color: #0284c7; font-size: 11px; font-weight: bold;")
        right_layout.addWidget(draw_label)
        self.canvas = IsolatedDrawingCanvas()
        right_layout.addWidget(self.canvas, stretch=1)
        self.splitter.addWidget(right_container)

        # Allocate 30% for reference image, 70% for expanded drawing zone
        self.splitter.setSizes([300, 700])
        main_layout.addWidget(self.splitter, stretch=1)

        # Task Submission Stream Triggers
        self.submit_btn = QPushButton(f"💾 TRANSMIT & COMPLETE {self.shape_type} ASSESSMENT TASK")
        self.submit_btn.setStyleSheet("""
            QPushButton {
                font-size: 14px; font-weight: bold; padding: 12px; 
                background-color: #10b981; color: white; border: none; border-radius: 4px;
            }
            QPushButton:hover { background-color: #059669; }
            QPushButton:pressed { background-color: #047857; }
        """)

        # Verified Submission Event Connection Hook
        self.submit_btn.clicked.connect(self.submit_data)
        main_layout.addWidget(self.submit_btn)

        # --- AUTHOR SEPARATOR AND ATTRIBUTION LABEL ---
        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setFrameShadow(QFrame.Shadow.Sunken)
        divider.setStyleSheet("background-color: #334155; max-height: 1px; border: none;")
        main_layout.addWidget(divider)

        author_label = QLabel("System Architecture & Algorithms Designed by: Engineer Syada & Patient Alvi Research Framework")
        author_label.setStyleSheet("font-size: 11px; color: #475569; font-weight: normal; font-style: italic;")
        author_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        main_layout.addWidget(author_label)
        # -----------------------------------------------

        main_central_widget.setLayout(main_layout)
        self.setCentralWidget(main_central_widget)

    def submit_data(self):
        payload = {
            "patientId": f"{self.patient_id}_{self.shape_type}",
            "rawKinematicData": json.dumps(self.canvas.kinematic_data)
        }
        try:
            SERVER_URL = "http://localhost:8080/api/v1/assessment/sessions"
            response = requests.post(SERVER_URL, json=payload, headers={"Content-Type": "application/json"}, timeout=5)
            response.raise_for_status()
            print(f"Data package pushed successfully for mapping: {self.shape_type}.")
        except Exception as e:
            print(f"Network error payload push failed: {e}")

        self.close()

if __name__ == "__main__":
    if len(sys.argv) >= 3:
        patient_base_id = sys.argv[1]
        shape_type = sys.argv[2]
    else:
        patient_base_id = "DEBUG_LOCAL_RUN"
        shape_type = "SPIRAL"

    app = QApplication(sys.argv)
    window = NeuroCaptureApp(patient_base_id, shape_type)
    window.showMaximized()
    sys.exit(app.exec())