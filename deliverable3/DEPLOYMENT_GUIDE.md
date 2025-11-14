
# 🚀 DEPLOYMENT GUIDE  
**TinyTroupe Simulation App – Deliverable 3**

This guide explains how to deploy, rebuild, and maintain the TinyTroupe Simulation App on HuggingFace Spaces (Docker mode).

---

# 📦 1. Requirements

- HuggingFace account  
- A new Space (set to **Docker** hardware type)
- GitHub repo containing the project files
- Dockerfile present in root directory  
- Internet connection

---

# 2. Installation (Local)

Clone repository:
```bash
git clone https://github.com/yourusername/tinytroupe-simulator.git
cd tinytroupe-simulator
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Run the app:

bash
Copy code
python app.py
# 3. Deploying on HuggingFace Spaces (Docker)
Step 1 — Create Space
Go to Spaces → New Space

Select:

SDK: Docker
Visibility: Public
Name: tinytroupe-simulator

Step 2 — Push Your Files
Include:

app.py
simulation_engine.py
personas.json
requirements.txt
Dockerfile
README.md
Documentation files

Use Git:

bash
Copy code
git remote add space https://huggingface.co/spaces/USERNAME/tinytroupe-simulator
git push space main
Step 3 — Let the container build
HuggingFace will:

Install dependencies
Build Docker image
Expose port 7860
Launch app
Build usually takes 2–4 minutes.

⚠️ 4. Common Deployment Issues
Issue	Solution
App stuck on “Building”	Reduce dependencies in requirements.txt
RuntimeError: HfFolder import error	Replace huggingface_hub version
App stuck on “Starting”	Ensure demo.launch(server_name="0.0.0.0")
Permission denied for ~/.config	Avoid packages like matplotlib that create config folders
JSON decode error	Validate personas.json using jsonlint.com

🔄 5. Updating the Live Space
After making changes:

bash
Copy code
git add .
git commit -m "Update app"
git push space main
The container will automatically rebuild.

🔧 6. Maintenance & Monitoring
Logs
Open → “Logs” tab on HuggingFace.
Rebuild Space
Sometimes helpful after dependency edits.
Click → Settings → Factory Reset
Version Control
Keep documentation and code in sync.

🔐 7. Security Recommendations
No external APIs → low risk
Input sanitized via .replace()
Personas stored locally (no database)
No user authentication required

🎉 8. Deployment Completed
If the app loads and the persona dropdown appears, your deployment is successful.

### 🚀 Live Deployment
Your live simulation app is available at:

👉 https://huggingface.co/spaces/YOUR_USERNAME/tinytroupe-simulator

