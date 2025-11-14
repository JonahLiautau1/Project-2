import json
import gradio as gr
from simulation_engine import run_simulation

def load_personas():
    """Load personas from personas.json safely."""
    try:
        with open("personas.json", "r") as f:
            return json.load(f)
    except Exception as e:
        return {"Error": {"name": "Error", "response_template": f"Failed to load personas: {e}"}}

# Load persona data
personas = load_personas()
persona_names = list(personas.keys())

def simulate(persona_id, message):
    """Run the simulation with proper handling."""
    try:
        persona_data = personas.get(persona_id)
        if persona_data is None:
            return f"Error: Persona '{persona_id}' not found."

        return run_simulation(persona_data, message)
    except Exception as e:
        return f"Simulation failed: {e}"

with gr.Blocks() as demo:
    gr.Markdown("## 🧠 TinyTroupe Simulation App (Simple & Reliable)")

    persona_input = gr.Dropdown(
        label="Choose Persona",
        choices=persona_names,
        value=persona_names[0] if persona_names else None
    )

    msg_input = gr.Textbox(
        label="Your Message",
        placeholder="Type something..."
    )

    output = gr.Textbox(label="Persona Response")

    simulate_button = gr.Button("Run Simulation")
    simulate_button.click(simulate, inputs=[persona_input, msg_input], outputs=output)

# Important: HuggingFace requires explicit host + port
demo.launch(server_name="0.0.0.0", server_port=7860)
