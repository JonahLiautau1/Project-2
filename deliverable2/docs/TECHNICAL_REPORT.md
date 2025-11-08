# Deliverable 2 — Technical Report

## Executive Summary
This beta demonstrates an agentic, persona-based simulation tool that product teams can use to evaluate features before build. Users enter a feature, select personas, run live conversations, and generate a synthesis. When API credits are unavailable, the app falls back to MOCK responses to ensure the full experience is demoable.

## Architecture
- **UI (Streamlit):** feature input, persona selection, live conversations, synthesis.
- **Engine (`simulation.py`):** OpenAI-backed chat with robust fallback to MOCK.
- **Personas Loader:** accepts YAML as dict **or** list; defaults provided if file missing/invalid.
- **State:** one `Conversation` per persona stored in `st.session_state`.

## Simulation Algorithm
1. Build a **system** message from persona metadata (tone, goals).
2. Add a persona-scoped **feature** system message.
3. Append **history** per persona and the new **user** prompt.
4. Engine calls OpenAI (if available) or returns a contextual **MOCK** reply.
5. Synthesis aggregates concerns, risks, and recommendations across personas.

## Live Conversation Capabilities
- Multi-persona selection (1–4)
- Real-time follow-ups
- Deterministic synthesis (no API required)
- Personas upload via YAML

## Use Cases & Examples
- **Scenario 1 — Dark Mode:** Priya (PM), Marco (New User), Avery (A11y) → [log](interactions/scenario1_dark_mode.md)
- **Scenario 2 — Onboarding:** Tessa (Power User), Lisa (DS) → [log](interactions/scenario2_onboarding.md)
- **Scenario 3 — Data Sharing:** Omar (DPO), Priya (PM), Marco (New User) → [log](interactions/scenario3_data_sharing.md)
- **Scenario 4 — Notifications:** Lisa (DS), Tessa (Power User) → [log](interactions/scenario4_notifications.md)

## Insights (Cross-Scenario)
- Recurring needs for clarity, discoverability, and measurable outcomes.
- A11y and DPO personas surface risks early (contrast, semantics, consent, retention).
- Power users request customization and speed; new users need progressive disclosure.

## Recommendations
- Start with a **small pilot** (20–50 users); instrument leading metrics.
- Tighten copy, reduce cognitive load; clear defaults + safe fallbacks.
- Make categories and toggles more discoverable; define success metrics up front.

## Instructor Feedback & Responses
- **Depth & Design:** Added architecture and algorithm sections.
- **Diversity of personas:** Included PM, DS, DPO, A11y, Power User, New User.
- **Error handling:** Implemented MOCK fallback and .env loading.
- **Live UI:** Added dynamic persona selection and history-based follow-ups.

## Future Enhancements
- Roundtable mode (personas react to each other)
- RAG over product docs; export to PDF
- Persona scoring and satisfaction metrics
- Cloud deployment and auth (Deliverable 3)

