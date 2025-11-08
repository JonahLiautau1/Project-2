# Deliverable 2 — Beta Version (Persona-Based Feature Simulation)

This folder contains the **beta version** of my persona-driven product simulation tool for CS676.  
The goal of Deliverable 2 is to demonstrate a working app that allows users to:

✅ Select personas  
✅ Enter product features  
✅ Ask follow-up questions  
✅ View live persona reactions  
✅ Generate a cross-persona synthesis  
✅ Review multiple real scenarios  
✅ Run the app even without OpenAI credits (MOCK mode)

---

## 📁 Contents of This Folder

| File/Folder | Description |
|-------------|-------------|
| **app.py** | Streamlit UI for running live simulations |
| **simulation.py** | Core simulation engine (OpenAI + MOCK fallback) |
| **personas.yaml** | Predefined persona database |
| **Deliverable2_Report.md** | Full technical report required for D2 |
| **README_D2.md** | (This file) How to run and understand the beta |
| **requirements.txt** | Python dependencies |
| **use_cases.md** | Summary of the 4 feature simulation scenarios |
| **instructor_feedback.md** | Instructor feedback + improvements made |
| **interactions/** | Folder containing all scenario transcripts |

---

## ▶️ How to Run the App (Local Instructions)

### 1. Install Python
Python **3.10+** required.

### 2. Install dependencies
From inside the repository:


### 3. (Optional) Add your OpenAI key  
Create a `.env` file inside `deliverable2/`:

**If no key or no credits**, the app automatically switches to **MOCK mode**, so the professor can run the app without errors.

### 4. Start the app
Run:
streamlit run app.py


The app opens at:
http://localhost:8501

---

## 💡 What This Beta Demonstrates

### ✅ 1. Persona selection  
User can pick multiple personas (PM, DS, New User, A11y, etc.).

### ✅ 2. Feature input  
PRD text, workflows, ideas, UI changes, etc.

### ✅ 3. Real-time conversation  
Ask a live question → persona responds in character.

### ✅ 4. Automatic fallback  
If OpenAI key is missing or out of credits → MOCK responses ensure grading is smooth.

### ✅ 5. Synthesis generation  
Aggregates multiple persona concerns, risks, and suggestions.

### ✅ 6. Multiple real feature scenarios  
All interactions stored in:
deliverable2/interactions/


Each file contains the recorded live conversation logs required for Deliverable 2.

---

## ✅ Instructor Feedback (Round 2)

The following improvements were implemented based on instructor feedback:

- Added more diverse personas  
- Added real use cases across industries  
- Improved technical depth of the simulation engine  
- Created a deterministic synthesis system  
- Added safe error handling + OpenAI fallback  
- Improved repository documentation and clarity  

---

## ✅ Next Steps (For Deliverable 3)

- Deploy to HuggingFace Spaces  
- Add persona-to-persona roundtable mode  
- Add better visualization of insights  
- Add RAG for PRD uploads  
- Add export to PDF  

---

## ✅ Summary

This beta demonstrates a fully functional persona simulation framework capable of:

⭐ Exploring feature designs  
⭐ Stress-testing product ideas  
⭐ Revealing usability issues early  
⭐ Supporting rapid product iteration  

The technical report (`Deliverable2_Report.md`) includes architecture, algorithm design, documentation, instructor feedback responses, and project insights.

---

# ✅ End of README_D2.md




