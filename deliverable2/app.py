import os
import time
import yaml
import streamlit as st
from simulation import load_personas, Conversation, SimulationEngine, synthesize_feedback

st.set_page_config(page_title="Persona Simulator — Beta", page_icon="🤖", layout="wide")

st.title("🤖 Persona-based Feature Simulation — Beta")

with st.sidebar:
    st.header("Settings")
    openai_key = st.text_input("OpenAI API Key", type="password", value=os.getenv("OPENAI_API_KEY", ""))
    if openai_key:
        os.environ["OPENAI_API_KEY"] = openai_key
    model = st.selectbox("Model", ["gpt-4.1-mini", "gpt-4o-mini", "gpt-4.1", "o4-mini"], index=0)
    temperature = st.slider("Temperature", 0.0, 1.0, 0.3, 0.1)
    personas_path = st.text_input("Personas file", value="personas.yaml")
    uploaded_yaml = st.file_uploader("Upload custom personas.yaml", type=["yaml", "yml"], accept_multiple_files=False)
    if uploaded_yaml:
        personas_path = "/tmp/_custom_personas.yaml"
        with open(personas_path, "wb") as f:
            f.write(uploaded_yaml.read())

# Load personas
try:
    personas = load_personas(personas_path)
except Exception as e:
    st.error(f"Failed to load personas: {e}")
    st.stop()

# Compose UI
cols = st.columns([1,2])
with cols[0]:
    st.subheader("Feature under test")
    feature = st.text_area("Describe the feature (paste PRD snippet, UI idea, workflow, etc.)", height=220, placeholder="Example: 'Dark Mode for mobile app with scheduled sunset-to-sunrise toggle and per-screen overrides.'")
    st.markdown("---")
    st.subheader("Pick personas")
    persona_keys = st.multiselect("Choose 1–4 personas to simulate", list(personas.keys()), default=["product_manager", "data_scientist", "accessibility_advocate"])
    st.caption("Tip: you can edit personas.yaml to add/modify personas.")

    st.markdown("---")
    st.subheader("Quick actions")
    simulate = st.button("Start conversations", type="primary")
    synth = st.button("Synthesize feedback (after a few messages)")

with cols[1]:
    st.subheader("Live conversations")
    if "sessions" not in st.session_state:
        st.session_state.sessions = {}

    if simulate:
        for key in persona_keys:
            card = personas[key]
            convo = Conversation(feature=feature, persona=card)
            st.session_state.sessions[key] = {"convo": convo, "engine": SimulationEngine(model=model, temperature=temperature)}

    # Render chat UIs
    for key in list(st.session_state.sessions.keys()):
        block = st.container(border=True)
        with block:
            card = personas.get(key)
            if not card:
                st.warning(f"Persona missing: {key}")
                continue
            st.markdown(f"**{card.name} — {card.role}**")            
            chat = st.session_state.sessions[key]["convo"]
            engine = st.session_state.sessions[key]["engine"]
            for t in chat.turns:
                st.chat_message("user" if t.who == "USER" else "assistant").write(t.text)
            prompt = st.chat_input(f"Chat with {card.name}...")
            if prompt:
                with st.spinner("Thinking..."):
                    reply = engine.ask(chat, prompt)
                st.chat_message("user").write(prompt)
                st.chat_message("assistant").write(reply)

    if synth and st.session_state.sessions:
        st.markdown("---")
        st.subheader("📋 Synthesized feedback")
        for key, pack in st.session_state.sessions.items():
            chat = pack["convo"]
            with st.spinner(f"Summarizing {chat.persona.name}..."):
                summ = synthesize_feedback(chat)["summary"]
            st.markdown(f"#### {chat.persona.name}")
            st.markdown(summ)
