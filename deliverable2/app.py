# app.py  — Persona-based Feature Simulation (Beta, D2 Final)

import os
import streamlit as st
from dotenv import load_dotenv

from simulation import (
    load_personas,
    Conversation,
    SimulationEngine,
    synthesize_feedback,
    build_system_message,
)

# ---- App setup ----
st.set_page_config(page_title="Persona Simulator — Beta", page_icon="🤖", layout="wide")
st.title("🤖 Persona-based Feature Simulation — Beta (Deliverable 2)")
load_dotenv()  # load .env so OPENAI_API_KEY can be found

# ---- Sidebar ----
with st.sidebar:
    st.header("Settings")
    # API key entry (optional; uses env if blank)
    existing_key = os.getenv("OPENAI_API_KEY", "")
    openai_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=existing_key if existing_key else "",
        help="Optional. If blank or out of quota, the app uses MOCK replies so you can still demo.",
    )
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key

    model = st.selectbox(
        "Model",
        ["gpt-4o-mini", "gpt-4.1-mini", "gpt-4.1", "o4-mini"],
        index=0,
        help="Use a lightweight model to keep cost low; MOCK replies are used if no credits.",
    )
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)

    personas_path = st.text_input("Personas file", value="personas.yaml")
    up = st.file_uploader("Upload custom personas.yaml", type=["yaml", "yml"])
    if up:
        personas_path = "/tmp/_custom_personas.yaml"
        with open(personas_path, "wb") as f:
            f.write(up.read())

# ---- Load personas safely ----
try:
    personas = load_personas(personas_path)
except Exception as e:
    st.error(f"Failed to load personas: {e}")
    st.stop()

# ---- Layout ----
left, right = st.columns([1, 1], gap="large")

with left:
    st.subheader("Feature under test")
    feature = st.text_area(
        "Paste a PRD snippet, UI idea, or workflow",
        height=200,
        placeholder="Example: 'Dark Mode with a sunset-to-sunrise schedule and per-screen overrides.'",
    )

    st.markdown("---")
    st.subheader("Pick personas")
    persona_choices = list(personas.keys())
    defaults = [x for x in ["product_manager", "new_user", "accessibility_advocate"] if x in persona_choices]
    if not defaults and persona_choices:
        defaults = persona_choices[:2]

    selected = st.multiselect(
        "Choose 1–4 personas",
        persona_choices,
        default=defaults,
        help="Hold Ctrl/Cmd to pick multiple.",
    )

    st.markdown("---")
    st.subheader("Live prompt to all selected personas")
    user_prompt = st.text_input(
        "Ask a question / give a task",
        placeholder="e.g., 'What confuses you about this feature? How would you improve it?'",
    )
    ask_btn = st.button("Ask all personas", type="primary", use_container_width=True)

with right:
    st.subheader("Live conversations")
    conversations_container = st.container()

# ---- Session state: one Conversation per persona ----
if "sessions" not in st.session_state:
    st.session_state.sessions = {}  # key -> Conversation

# Lazily create conversations for selected personas
for key in selected:
    if key not in st.session_state.sessions:
        st.session_state.sessions[key] = Conversation()

# ---- Engine ----
engine = SimulationEngine(model=model, temperature=temperature)

# ---- Ask all personas ----
if ask_btn:
    if not feature.strip():
        st.warning("Please enter a feature description first.")
    elif not selected:
        st.warning("Please select at least one persona.")
    elif not user_prompt.strip():
        st.warning("Please enter your question/prompt.")
    else:
        for key in selected:
            persona_def = personas.get(key, {})
            convo: Conversation = st.session_state.sessions[key]

            # Build messages
            system_msg = build_system_message(persona_def)
            persona_msg = {"role": "system", "content": f"Feature under test:\n{feature}"}

            # Get reply (falls back to MOCK when API is missing/over quota)
            reply = engine.ask(system=system_msg, persona=persona_msg, history=convo.to_messages(), prompt=user_prompt)

            # Append to transcript
            convo.add("user", user_prompt)
            convo.add("assistant", reply)

        st.success("Responses added. See each persona thread on the right.")

# ---- Render conversations ----
with conversations_container:
    if not selected:
        st.info("Select personas on the left to view conversations.")
    else:
        for key in selected:
            persona_def = personas.get(key, {})
            display_name = persona_def.get("name", key)
            with st.expander(f"🧑 Persona: {display_name}", expanded=True):
                convo: Conversation = st.session_state.sessions[key]
                if not convo.history:
                    st.caption("No messages yet. Ask a question on the left.")
                else:
                    for m in convo.history:
                        if m["role"] == "user":
                            st.markdown(f"**You:** {m['content']}")
                        else:
                            st.markdown(m["content"])

# ---- Synthesis ----
st.markdown("---")
st.subheader("Synthesize feedback (after a few exchanges)")
c1, _ = st.columns([1, 2])
with c1:
    synth_btn = st.button("Generate synthesis", use_container_width=True)

if synth_btn:
    subset = {k: st.session_state.sessions[k] for k in selected if k in st.session_state.sessions}
    if not subset:
        st.info("Nothing to synthesize yet. Start a conversation first.")
    else:
        summary = synthesize_feedback(subset)
        st.markdown(summary)

st.caption("Tip: If you don’t have API credits, the app automatically uses **MOCK** replies so you can still demo.")

      
