from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="operator")
    points = Column(Integer, default=0)

    jobs = relationship("Job", back_populates="operator")

class Job(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    part_number = Column(String, index=True)
    description = Column(String, nullable=True)
    due_date = Column(DateTime, nullable=True)
    status = Column(String, default="unclaimed")
    operator_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    hot = Column(Boolean, default=False)

    operator = relationship("User", back_populates="jobs")
    history = relationship("JobHistory", back_populates="job")

class JobHistory(Base):
    __tablename__ = "job_history"

    id = Column(Integer, primary_key=True, index=True)
    job_id = Column(Integer, ForeignKey("jobs.id"))
    timestamp = Column(DateTime, default=datetime.utcnow)
    event = Column(String)

    job = relationship("Job", back_populates="history")
