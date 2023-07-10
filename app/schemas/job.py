from datetime import date
from typing import Any
from fastapi import Form
from pydantic import BaseModel


class JobCreate(BaseModel):
    description: str
    job_type: str
    career: str
    city: str
    company_id: int

    class Config:
        orm_mode = True


class JobCreateForm(BaseModel):
    description: str
    job_type: str
    career: str
    city: str
    company_id: int

    @classmethod
    def as_form(
        cls,
        description: str = Form(...),
        job_type: str = Form(...),
        career: str = Form(...),
        city: str = Form(...),
        company_id: int = Form(...),
    ) -> "JobCreateForm":
        return cls(
            description=description,
            job_type=job_type,
            career=career,
            city=city,
            company_id=company_id,
        )


class JobEditForm(BaseModel):
    description: str
    job_type: str
    career: str
    city: str

    @classmethod
    def as_form(
        cls,
        description: str = Form(...),
        job_type: str = Form(...),
        career: str = Form(...),
        city: str = Form(...),
    ) -> "JobEditForm":
        return cls(
            description=description,
            job_type=job_type,
            career=career,
            city=city,
        )


class Job(JobCreate):
    id: int
    active: bool
    city_id: int
    career_id: int
    file_id: int = None
    creation_date: date

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

    class Config:
        orm_mode = True
