from fastapi import FastAPI, HTTPException
from typing import List, Dict
from datetime import datetime, timezone

app = FastAPI(title="Hybrid Production Scheduler")

_users: List[dict] = []
_jobs: List[dict] = []
_next_user_id = 1
_next_job_id = 1


def utc_now() -> datetime:
    """Return the current UTC time as a naive datetime."""
    return datetime.now(timezone.utc).replace(tzinfo=None)


def _find_user(username: str):
    for u in _users:
        if u["username"] == username:
            return u
    return None


@app.post("/users/")
def create_user(user: Dict):
    global _next_user_id
    if _find_user(user["username"]):
        raise HTTPException(status_code=400, detail="username already registered")
    db_user = {
        "id": _next_user_id,
        "username": user["username"],
        "role": user.get("role", "operator"),
        "points": 0,
    }
    _next_user_id += 1
    _users.append(db_user)
    return db_user


@app.get("/users/")
def list_users():
    return _users


@app.get("/leaderboard")
def leaderboard():
    return sorted(_users, key=lambda u: u.get("points", 0), reverse=True)


@app.get("/users/{username}")
def get_user(username: str):
    user = _find_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user


@app.get("/users/{username}/jobs")
def get_user_jobs(username: str):
    user = _find_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return [j for j in _jobs if j.get("operator_id") == user["id"]]

@app.get("/jobs/")
def read_jobs():
    return _jobs


@app.get("/jobs/{job_id}")
def read_job(job_id: int):
    job_id = int(job_id)
    job = next((j for j in _jobs if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    return job


@app.delete("/jobs/{job_id}")
def delete_job(job_id: int):
    job_id = int(job_id)
    index = next((i for i, j in enumerate(_jobs) if j["id"] == job_id), None)
    if index is None:
        raise HTTPException(status_code=404, detail="job not found")
    job = _jobs.pop(index)
    return job


@app.get("/jobs/hot")
def read_hot_jobs():
    hot_jobs = []
    now = utc_now()
    for job in _jobs:
        if job.get("hot"):
            hot_jobs.append(job)
            continue
        due = job.get("due_date")
        if due:
            try:
                due_dt = datetime.fromisoformat(due)
                if (due_dt - now).total_seconds() <= 24 * 3600:
                    hot_jobs.append(job)
            except ValueError:
                pass
    return hot_jobs


@app.post("/jobs/")
def create_job(job: Dict):
    global _next_job_id
    created = utc_now().isoformat()
    record = {
        "part_number": job.get("part_number"),
        "description": job.get("description"),
        "due_date": job.get("due_date"),
        "hot": job.get("hot", False),
        "id": _next_job_id,
        "status": "unclaimed",
        "operator_id": None,
        "created_at": created,
        "completed_at": None,
        "history": [{"timestamp": created, "event": "created"}],
    }
    _next_job_id += 1
    _jobs.append(record)
    return record


@app.post("/jobs/claim")
def claim_job(payload: Dict):
    job_id = int(payload.get("job_id"))
    job = next((j for j in _jobs if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    user = _find_user(payload.get("username"))
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    job["status"] = "running"
    job["operator_id"] = user["id"]
    job["history"].append({"timestamp": utc_now().isoformat(), "event": f"claimed by {user['username']}"})
    return job


@app.post("/jobs/unclaim")
def unclaim_job(payload: Dict):
    job_id = int(payload.get("job_id"))
    job = next((j for j in _jobs if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    job["status"] = "unclaimed"
    job["operator_id"] = None
    job["history"].append({"timestamp": utc_now().isoformat(), "event": "unclaimed"})
    return job


@app.post("/jobs/complete")
def complete_job(payload: Dict):
    job_id = int(payload.get("job_id"))
    job = next((j for j in _jobs if j["id"] == job_id), None)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    job["status"] = "finished"
    job["completed_at"] = utc_now().isoformat()
    job["history"].append({"timestamp": job["completed_at"], "event": "completed"})
    if job["operator_id"] is not None:
        user = next((u for u in _users if u["id"] == job["operator_id"]), None)
        if user:
            points = 1 + (1 if job.get("hot") else 0)
            due = job.get("due_date")
            if due:
                try:
                    if utc_now() <= datetime.fromisoformat(due):
                        points += 1
                except ValueError:
                    pass
            user["points"] += points
    return job


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
