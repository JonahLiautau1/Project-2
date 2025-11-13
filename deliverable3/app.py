import json
import traceback
from simulation_engine import run_simulation
from utils.logging_setup import logger

def load_personas():
    try:
        with open("personas.json", "r") as f:
            personas = json.load(f)
        return personas
    except Exception as e:
        logger.error(f"Failed to load personas: {e}")
        raise

def main():
    print("=== TinyTroupe Persona Simulation App (Deliverable 3) ===")
    personas = load_personas()

    print("\nAvailable Personas:")
    for p in personas:
        print(f"- {p['id']}: {p['name']} ({p['profile']['role']})")

    try:
        persona_id = input("\nEnter persona ID to simulate: ").strip()
        scenario = input("Enter scenario text: ").strip()

        output = run_simulation(persona_id, scenario)
        print("\n--- Simulation Output ---")
        print(output)

    except Exception as e:
        logger.error(f"Simulation error: {e}")
        traceback.print_exc()

if __name__ == "__main__":
    main()
