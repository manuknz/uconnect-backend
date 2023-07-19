from datetime import date
from typing import Any, Dict, List, Optional
from fastapi import Form
from pydantic import BaseModel, Field


class Skill(BaseModel):
    skill_name: str
    experience: str


class JobCreateWithoutImage(BaseModel):
    description: str
    job_type: str
    career: str
    city: str
    company_id: int
    skills: Optional[List[Skill]]

    class Config:
        orm_mode = True


class JobEdit(BaseModel):
    description: str
    job_type: str
    career: str
    city: str
    skills: Optional[List[Skill]]

    class Config:
        orm_mode = True


class JobResponse(BaseModel):
    id: int
    description: str
    job_type: str
    career_name: str
    city_name: str
    company_id: int
    active: bool
    file_id: int = None
    creation_date: date
    skills: Optional[List[Skill]]

    class Config:
        orm_mode = True
