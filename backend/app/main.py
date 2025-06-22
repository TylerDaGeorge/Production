from fastapi import FastAPI

app = FastAPI(title="Hybrid Production Scheduler")

_jobs: list[dict] = []
_next_id = 1

@app.get("/jobs/")
def read_jobs() -> list[dict]:
    """Return all jobs."""
    return _jobs

@app.post("/jobs/")
def create_job(job: dict) -> dict:
    """Create a new job and add it to the in-memory list."""
    global _next_id
    job = job.copy()
    job.setdefault("status", "unclaimed")
    job["id"] = _next_id
    _next_id += 1
    _jobs.append(job)
    return job

@app.post("/jobs/claim")
def claim_job(payload: dict) -> dict:
    """Mark a job as claimed by a user."""
    job_id = payload.get("job_id")
    username = payload.get("username")
    for job in _jobs:
        if job["id"] == job_id:
            job["status"] = "running"
            job["operator"] = username
            return job
    return {"error": "job not found"}

@app.post("/jobs/complete")
def complete_job(payload: dict) -> dict:
    """Mark a job as completed."""
    job_id = payload.get("job_id")
    for job in _jobs:
        if job["id"] == job_id:
            job["status"] = "finished"
            return job
    return {"error": "job not found"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
