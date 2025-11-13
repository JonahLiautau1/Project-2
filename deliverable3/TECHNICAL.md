# TECHNICAL DOCUMENTATION – Deliverable 3
## TinyTroupe Persona Simulation App
### CS 676 – Fall 2025

---

# 1. System Architecture Overview

The TinyTroupe Simulation App is a modular Python application designed to simulate realistic persona feedback for product features. The Deliverable 3 version is production-ready, containerized, and suitable for deployment on HuggingFace Spaces.

### Core Components
- **app.py**  
  CLI entry point for running persona simulations. Handles input, validation, and output formatting.

- **simulation_engine.py**  
  Core simulation logic that retrieves persona details, processes scenarios, and generates TinyTroupe-style responses.

- **personas.json**  
  Finalized database of realistic personas including behavioral traits, tone, and demographic information.

- **utils/logging_setup.py**  
  Centralized logging configuration using `loguru`, supporting debugging and auditability.

- **tests/**  
  Pytest-based automated tests for simulation engine and persona integrity.

---

# 2. Data Flow Diagram

```
┌───────────────┐       ┌────────────────────┐       ┌─────────────────────────┐
│   app.py      │──────▶│ simulation_engine.py│──────▶│ Persona-based Response │
└───────────────┘       └────────────────────┘       └─────────────────────────┘
        │                         │ 
        ▼                         ▼
 ┌───────────────┐         ┌────────────────────┐
 │ personas.json │◀────────│ logging_setup.py   │
 └───────────────┘         └────────────────────┘
```

---

# 3. Persona Schema Description

Each persona in `personas.json` follows:

```json
{
  "id": "persona_01",
  "name": "Alicia Ramirez",
  "profile": {
    "age": 29,
    "role": "Tech-Comfortable Mobile User",
    "tech_level": "intermediate",
    "tone": "friendly and concise",
    "style": "practical, direct feedback",
    "behavior": "Alicia quickly identifies usability problems and values speed."
  }
}
```

**Field Requirements**
| Field | Type | Description |
|-------|------|-------------|
| id | string | Unique persona identifier |
| name | string | Persona name |
| profile | object | Characteristics and behavioral attributes |
| tone | string | Preferred communication tone |
| style | string | Feedback behavior |
| behavior | string | TinyTroupe-like descriptive pattern |

---

# 4. Simulation Engine Logic

### Steps:
1. **Load personas** from JSON  
2. **Select persona** by ID  
3. **Inject scenario text**  
4. **Generate simulated feedback**  
   - Based on persona’s tone  
   - Based on persona’s style  
   - Based on behavioral tendencies  
5. **Return formatted response** to CLI or UI  

### Algorithmic Flow

```
load_personas()
    └── find persona by ID
            └── inject scenario
                    └── generate persona-specific output
```

---

# 5. Error Handling Strategy

- Missing persona → clear ValueError with logging  
- Corrupted JSON → logs error + stops execution  
- Empty scenario → prompted error  
- All errors logged in `simulation.log` via Loguru  

---

# 6. Logging & Monitoring

- Logs stored in `simulation.log`
- Rotation at 1MB prevents large file issues
- Debug, info, and error logs captured

---

# 7. Container Architecture

The application runs inside a Docker container:

- Base image: `python:3.10`
- All dependencies installed via `requirements.txt`
- Entry point: `CMD ["python", "app.py"]`
- No OS-level dependencies required

---

# 8. Performance Considerations

- Lightweight JSON loading  
- O(1) persona lookup time in this implementation  
- Modular design for scaling to hundreds of personas  

---

# 9. Future Extensions

- Replace mocked TinyTroupe logic with real API calls  
- Streamlit UI for real-time simulation  
- Add persona clustering model  
- Persona evolution based on scenario history  
