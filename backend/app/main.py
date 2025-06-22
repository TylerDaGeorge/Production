from fastapi import FastAPI, HTTPException

from typing import List, Dict, Optional

from typing import List, Dict

app = FastAPI(title="Hybrid Production Scheduler")

_users: List[dict] = []
_jobs: List[dict] = []
_next_user_id = 1
_next_job_id = 1


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


@app.get("/users/{username}")
def get_user(username: str):
    user = _find_user(username)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user

@app.get("/jobs/")
def read_jobs():
    return _jobs


@app.post("/jobs/")
def create_job(job: Dict):
    global _next_job_id
    record = {
        "part_number": job.get("part_number"),
        "description": job.get("description"),
        "due_date": job.get("due_date"),
        "hot": job.get("hot", False),
        "id": _next_job_id,
        "status": "unclaimed",
        "operator_id": None,
        "history": [],
    }
    _next_job_id += 1
    _jobs.append(record)
    return record


@app.post("/jobs/claim")
def claim_job(payload: Dict):
    job = next((j for j in _jobs if j["id"] == payload.get("job_id")), None)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    user = _find_user(payload.get("username"))
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    job["status"] = "running"
    job["operator_id"] = user["id"]
    return job


@app.post("/jobs/complete")
def complete_job(payload: Dict):
    job = next((j for j in _jobs if j["id"] == payload.get("job_id")), None)
    if not job:
        raise HTTPException(status_code=404, detail="job not found")
    job["status"] = "finished"
    if job["operator_id"] is not None:
        user = next((u for u in _users if u["id"] == job["operator_id"]), None)
        if user:
            points = 1 + (1 if job.get("hot") else 0)
            user["points"] += points
    return job


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
