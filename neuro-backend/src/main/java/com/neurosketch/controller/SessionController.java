package com.neurosketch.backend.controller;

import com.neurosketch.backend.model.DrawingSession;
import com.neurosketch.backend.repository.DrawingSessionRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

import java.util.List;
import java.util.Map;

@RestController
@RequestMapping("/api/v1/assessment")
@CrossOrigin(origins = "*")
public class SessionController {

    @Autowired
    private DrawingSessionRepository repository;

    @PostMapping("/sessions")
    public ResponseEntity<?> saveSession(@RequestBody Map<String, String> payload) {
        try {
            String patientIdStr = payload.get("patientId");
            String rawKinematicData = payload.get("rawKinematicData");

            if (patientIdStr == null || rawKinematicData == null) {
                return ResponseEntity.badRequest().body("{\"error\":\"Missing required payload keys.\"}");
            }

            String testType = "UNKNOWN";
            if (patientIdStr.contains("_")) {
                String[] parts = patientIdStr.split("_");
                testType = parts[parts.length - 1];
            }

            DrawingSession session = new DrawingSession(patientIdStr, testType, rawKinematicData);
            repository.save(session);

            return ResponseEntity.ok().body("{\"status\":\"success\",\"message\":\"Kinematics saved to database core.\"}");
        } catch (Exception e) {
            return ResponseEntity.internalServerError().body("{\"error\":\"" + e.getMessage() + "\"}");
        }
    }

    @GetMapping("/sessions")
    public ResponseEntity<List<DrawingSession>> getAllSessions() {
        List<DrawingSession> sessions = repository.findAll();
        return ResponseEntity.ok(sessions);
    }
}