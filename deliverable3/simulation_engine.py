def run_simulation(persona, message):
    """
    Simple reliable persona engine.
    Fills the persona's response template with the user's input.
    """
    name = persona.get("name", "Unknown Persona")
    template = persona.get("response_template", "I received your message: {input}")

    # Replace placeholder safely
    response = template.replace("{input}", message)

    return f"[{name}] {response}"
