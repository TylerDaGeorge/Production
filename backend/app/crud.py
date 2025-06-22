from sqlalchemy.orm import Session
from . import models, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# User operations

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = pwd_context.hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password, role=user.role)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Job operations

def create_job(db: Session, job: schemas.JobCreate):
    db_job = models.Job(**job.dict())
    db.add(db_job)
    db.commit()
    db.refresh(db_job)
    db_history = models.JobHistory(job_id=db_job.id, event="created")
    db.add(db_history)
    db.commit()
    return db_job

def get_jobs(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Job).offset(skip).limit(limit).all()

def get_job(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()

def claim_job(db: Session, job: models.Job, user: models.User):
    job.status = "running"
    job.operator_id = user.id
    db_history = models.JobHistory(job_id=job.id, event=f"claimed by {user.username}")
    db.add(db_history)
    db.commit()
    db.refresh(job)
    return job

def complete_job(db: Session, job: models.Job):
    job.status = "finished"
    db_history = models.JobHistory(job_id=job.id, event="completed")
    db.add(db_history)
    db.commit()
    db.refresh(job)
    return job
