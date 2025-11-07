# Technical Report — Algorithm & Design (Draft)

## 1. Architecture Overview
- **UI**: Streamlit app (`app.py`) renders a multi-chat workspace; each persona has its own session.
- **Engine**: `SimulationEngine` wraps OpenAI Chat Completions with a system primer and persona card constraints.
- **Personas**: YAML-backed, with goals/fears/style/constraints shaping behavior; users can upload custom YAML.
- **Synthesis**: After some turns, we call the model to produce a structured summary (pros/cons/open questions/recommendation).

## 2. Persona Modeling
Each persona card has: `name, role, goals, fears, style, constraints, domain_expertise`.
At runtime, we inject:
1) A global system primer describing the task;
2) The selected persona card;
3) The running chat history.

This yields consistent persona behavior while allowing flexible prompts.

## 3. Conversation Loop
For each chat:
- User types a message (e.g., “List top 3 risks”).
- Engine composes messages = [system, persona, history] and requests a completion.
- Response is appended; UI redraws.

## 4. Feedback Synthesis
We convert the chat transcript to a single string and ask a small model for:
- Top 3 pros, Top 3 cons/risks
- Open questions
- Single-sentence recommendation

## 5. Decision-Making Process
- The persona cards bias the analysis (e.g., DPO emphasizes retention/consent).
- The global primer enforces a standard output style.
- The user can solicit an explicit decision at any time; synthesis also proposes one.

## 6. Extensibility
- Add personas to `personas.yaml` or upload a custom YAML at runtime.
- Swap the chat model, adjust temperature, or add tools (retrieval, calculators) in `SimulationEngine`.
- Export: you can save transcripts to Markdown (future work item).

## 7. Limitations / Future Enhancements
- Determinism is limited; consider function-calling for structured outputs.
- No backend persistence yet; add a DB or local JSON logs.
- Single-turn summarizer; could support multi-persona cross-review panels.
- Add automated evaluations (toxicity, hallucination guards).

## 8. Security & Privacy
- Keep secrets in `.env` (never commit).
- Avoid sending sensitive data in prompts; consider redaction middleware.
