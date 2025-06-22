from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class JobHistoryBase(BaseModel):
    timestamp: datetime
    event: str

class JobHistory(JobHistoryBase):
    id: int
    class Config:
        orm_mode = True

class JobBase(BaseModel):
    part_number: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    hot: bool = False

class JobCreate(JobBase):
    pass

class Job(JobBase):
    id: int
    status: str
    operator_id: Optional[int]
    history: List[JobHistory] = []

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str
    role: Optional[str] = "operator"

class User(UserBase):
    id: int
    role: str
    points: int

    class Config:
        orm_mode = True


class JobClaim(BaseModel):
    job_id: int
    username: str


class JobComplete(BaseModel):
    job_id: int
