import json
import traceback
from utils.logging_setup import logger

def load_personas():
    try:
        with open("personas.json", "r") as f:
            return json.load(f)
    except Exception as e:
        logger.error(f"Error loading personas: {e}")
        raise

def get_persona(persona_id):
    personas = load_personas()
    for p in personas:
        if p["id"] == persona_id:
            return p
    raise ValueError(f"Persona '{persona_id}' not found")

def run_simulation(persona_id, scenario):
    try:
        persona = get_persona(persona_id)
        logger.info(f"Running simulation for persona: {persona_id}")

        # TinyTroupe-like simulation behavior (mocked for deliverable)
        response = (
            f"[Persona: {persona['name']}]\n"
            f"Tone: {persona['profile']['tone']}\n"
            f"Feedback Style: {persona['profile']['style']}\n\n"
            f"Scenario Response:\n"
            f"{persona['profile']['behavior']} reacting to:\n'{scenario}'"
        )
        return response

    except Exception as e:
        logger.error(f"Simulation Engine Error: {e}")
        traceback.print_exc()
        raise
