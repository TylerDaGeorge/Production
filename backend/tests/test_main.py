# Ensure the project root is on the import path so that ``app`` can be
# discovered when tests run from the ``tests`` directory.
import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient
from fastapi import HTTPException
from app.main import app
from datetime import datetime, timedelta
import pytest

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

    # user should have earned points
    response = client.get("/users/alice")
    assert response.status_code == 200
    assert response.json()["points"] >= 1


def test_hot_jobs_and_leaderboard():
    client.post("/users/", json={"username": "bob"})
    client.post("/users/", json={"username": "carol"})
    due = (datetime.utcnow() + timedelta(hours=1)).isoformat()
    response = client.post(
        "/jobs/",
        json={"part_number": "XYZ", "hot": True, "due_date": due},
    )
    job = response.json()
    client.post("/jobs/claim", json={"job_id": job["id"], "username": "bob"})
    client.post("/jobs/complete", json={"job_id": job["id"]})

    leaderboard = client.get("/leaderboard").json()
    assert leaderboard[0]["username"] == "bob"
    assert leaderboard[0]["points"] >= 3

    hot_jobs = client.get("/jobs/hot").json()
    assert any(j["id"] == job["id"] for j in hot_jobs)


def test_unclaim_and_job_detail():
    client.post("/users/", json={"username": "dave"})
    job = client.post("/jobs/", json={"part_number": "123"}).json()
    jid = job["id"]
    client.post("/jobs/claim", json={"job_id": jid, "username": "dave"})

    detail = client.get(f"/jobs/{jid}").json()
    assert detail["status"] == "running"

    unclaimed = client.post("/jobs/unclaim", json={"job_id": jid}).json()
    assert unclaimed["status"] == "unclaimed"
    assert unclaimed["operator_id"] is None

    detail = client.get(f"/jobs/{jid}").json()
    events = [h["event"] for h in detail["history"]]
    assert "unclaimed" in events


def test_job_detail_not_found():
    with pytest.raises(HTTPException):
        client.get("/jobs/9999")
