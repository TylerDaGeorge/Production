# Frontend UI

This directory contains a very small HTML page used to interact with the
FastAPI backend. It relies only on browser JavaScript and can be served
with Python's built-in HTTP server.

## Usage

1. Make sure the backend API is running:
   ```bash
   cd backend/app
   python main.py  # or `uvicorn app.main:app` if uvicorn is installed
   ```
   The API will be available at `http://localhost:8000`.

2. Serve this UI (from the repository root):
   ```bash
   python -m http.server 8080 -d frontend
   ```
   Then open your browser to [http://localhost:8080](http://localhost:8080).

The UI allows you to create jobs and claim/complete them using the existing
API endpoints.
