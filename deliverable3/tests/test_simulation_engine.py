import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from simulation_engine import run_simulation

def test_simulation_basic():
    output = run_simulation("persona_01", "Test scenario")
    assert "Scenario Response" in output
