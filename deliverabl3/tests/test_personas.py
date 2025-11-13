import json

def test_personas_load():
    with open("personas.json") as f:
        personas = json.load(f)
    assert len(personas) > 0
