# Deliverable 3 – Final Container-Ready Simulation App

This deliverable contains a production-ready version of the TinyTroupe Simulation App.

## Included Features
- Docker-based container deployment
- Finalized persona database
- Simulation engine with logging + error handling
- Full technical documentation
- Testing results
- HuggingFace deployment guide

## How to Run Locally
```bash
pip install -r requirements.txt
python app.py

## How to Build Docker Image
docker build -t simulation-app .
docker run -p 7860:7860 simulation-app

