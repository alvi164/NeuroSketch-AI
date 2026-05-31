package com.neurosketch.backend.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.List;

@Entity
@Table(name = "drawing_sessions")
public class DrawingSession {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String patientId;
    private LocalDateTime timestamp;
    private String testType; // e.g., "Archimedean_Spiral", "Clock_Test"
    
    @Lob // Large Object storage for the serialized continuous array stream
    @Column(columnDefinition = "TEXT")
    private String rawKinematicData;

    // Constructors
    public DrawingSession() {
        this.timestamp = LocalDateTime.now();
    }

    public DrawingSession(String patientId, String testType, String rawKinematicData) {
        this.patientId = patientId;
        this.testType = testType;
        this.rawKinematicData = rawKinematicData;
        this.timestamp = LocalDateTime.now();
    }

    // Getters and Setters
    public Long getId() { return id; }
    public String getPatientId() { return patientId; }
    public void setPatientId(String patientId) { this.patientId = patientId; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public String getTestType() { return testType; }
    public void setTestType(String testType) { this.testType = testType; }
    public String getRawKinematicData() { return rawKinematicData; }
    public void setRawKinematicData(String rawKinematicData) { this.rawKinematicData = rawKinematicData; }
}