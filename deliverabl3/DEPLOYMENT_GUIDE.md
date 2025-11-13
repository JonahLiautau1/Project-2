# DEPLOYMENT GUIDE – Deliverable 3
## Deploying the TinyTroupe Simulation App to HuggingFace Spaces

---

# 1. Prerequisites
- HuggingFace account  
- GitHub repo containing deliverable3  
- Dockerfile (already included)  
- requirements.txt  

---

# 2. Deployment Overview

The app runs inside a Docker container, so HuggingFace Spaces handles:

- Building the Docker image  
- Starting the container  
- Monitoring logs  
- Allowing restart on failure  

---

# 3. Step-by-Step Deployment

### Step 1 — Create a New HuggingFace Space
1. Go to https://huggingface.co/spaces  
2. Click **Create Space**  
3. Choose:
   - **Space SDK** → **Docker**
   - **Name:** `your-username/tinytroupe-simulator`
   - **Visibility:** Public  

---

### Step 2 — Upload Your Deliverable 3 Files

You must upload these files:

```
app.py
simulation_engine.py
personas.json
requirements.txt
Dockerfile
utils/
tests/
```

Upload them into the Space.

---

### Step 3 — Wait for the Docker Build

HuggingFace automatically runs:

```
docker build .
docker run container
```

Watch the **Logs** panel for:

- Installing dependencies  
- Running the app  
- Any Python errors  

---

### Step 4 — Testing Deployment

In the Space:

1. Open the app  
2. Choose a persona  
3. Enter a scenario  
4. Confirm simulation output displays correctly  

---

# 4. Updating the Space

To deploy updates:

- Push new changes to GitHub  
- Re-upload changed files to HuggingFace  
OR  
- Connect HuggingFace Space to GitHub repo  

---

# 5. Troubleshooting

### ❗ Module Not Found  
→ Make sure file path matches import in `app.py`.

### ❗ Docker build fails  
→ Check requirements.txt for version conflicts.

### ❗ App crashes on startup  
→ Check simulation_engine imports.  
→ Look at error in HuggingFace logs.

---

# 6. Backup Procedures

- Keep `personas.json` backed up in GitHub  
- Maintain a versioned CHANGELOG.md  
- Log files rotate automatically  

---

# 7. Security Notes

- Do not commit API keys  
- If using TinyTroupe API in future:
  - Use `.env`
  - Add variables under HuggingFace **“Secrets”**

