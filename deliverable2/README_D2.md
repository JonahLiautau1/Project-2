# Deliverable 2 — Persona Simulator (Beta)

This is a beta app that demonstrates multi-persona simulation with live conversations and structured feedback.

## Quickstart
```bash
# 1) Create env
python -m venv .venv && source .venv/bin/activate  # (Windows: .venv\Scripts\activate)

# 2) Install deps
pip install -r requirements.txt

# 3) Set your API key
cp .env.example .env && echo 'Add your key to .env'

# 4) Run
streamlit run app.py
```

## Features
- Multiple predefined personas (edit `personas.yaml`) and custom persona upload
- Live, parallel chat UIs — each persona keeps context per feature
- One-click synthesis: pros/cons, open questions, and a recommendation
- Model/temperature selectable in the UI
- Clean repository layout (app, engine, personas, docs)

## Notes
- Never commit `.env` — rotate if already committed.
- Replace model names with organization defaults if needed.

## Folder layout
```
deliverable2_beta/
├─ app.py               # Streamlit front-end
├─ simulation.py        # Engine, persona model, summarizer
├─ personas.yaml        # Predefined personas
├─ requirements.txt
├─ .env.example
└─ docs/
   ├─ TECHNICAL_REPORT.md
   ├─ USE_CASES.md
   └─ INSTRUCTOR_FEEDBACK.md
```
