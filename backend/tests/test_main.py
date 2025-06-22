# Ensure the project root is on the import path so that ``app`` can be
# discovered when tests run from the ``tests`` directory.
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_read_jobs_empty():
    response = client.get("/jobs/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_job_and_flow():
    # create a user to claim jobs
    response = client.post("/users/", json={"username": "alice", "password": "pw"})
    assert response.status_code == 200

    # create a new job
    response = client.post("/jobs/", json={"part_number": "ABC123"})
    assert response.status_code == 200
    job = response.json()
    assert job["id"] == 1
    assert job["status"] == "unclaimed"

    # verify job list contains the new job
    response = client.get("/jobs/")
    assert response.json()[0]["id"] == 1

    # claim the job
    response = client.post("/jobs/claim", json={"job_id": 1, "username": "alice"})
    assert response.json()["status"] == "running"

    # complete the job
    response = client.post("/jobs/complete", json={"job_id": 1})
    assert response.json()["status"] == "finished"

