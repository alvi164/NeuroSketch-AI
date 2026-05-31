package com.neurosketch.backend.repository;

import com.neurosketch.backend.model.DrawingSession;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface DrawingSessionRepository extends JpaRepository<DrawingSession, Long> {
}