from datetime import date
from typing import Any
from pydantic import BaseModel


class JobCreate(BaseModel):
    description: str
    job_type: str
    creation_date: date
    career: str
    city: str
    file: Any
    id: int
    company_id: int

    class Config:
        orm_mode = True


class Job(JobCreate):
    id: int
    career_id: int
    city_id: int
    file_id: int
    active: bool

    class Config:
        orm_mode = True