# TESTING RESULTS – Deliverable 3

This file documents the outcome of functional and unit tests for the TinyTroupe Simulation App.

---

# 1. Test Suite Overview

Tests located in:

```
deliverable3/tests/
```

Includes:
- test_personas.py
- test_simulation_engine.py

---

# 2. Testing Commands

Tests executed using:

```bash
pytest
```

---

# 3. Results

======================================= test session starts ========================================
platform linux -- Python 3.12.1, pytest-8.4.2, pluggy-1.6.0
rootdir: /workspaces/Project-2/deliverable3
plugins: anyio-4.11.0
collected 2 items

tests/test_personas.py .                                  [ 50%]
tests/test_simulation_engine.py .                         [100%]

========================================= 2 passed in 0.15s =========================================



---

# 4. Interpretation

- All tests passed successfully  
- Persona database loads correctly  
- Simulation engine produces expected output  

---

# 5. Validation Summary

The model is functional, stable, and ready for deployment.

