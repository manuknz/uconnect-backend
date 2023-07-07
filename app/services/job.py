from datetime import datetime
import logging
from tkinter import N
from typing import List
from fastapi import HTTPException, UploadFile, File, status

from sqlalchemy.orm import Session

from app.models import career, job as models
from app.schemas import job as schemas

from app.services import career as career_services
from app.services import city as city_services
from app.services import company as company_services
from app.services import file as file_services
from app.utils.ErrorMessage import ErrorMessage


logger = logging.getLogger(__name__)


def get_jobs(db: Session, career_id: int, job_type: str, skills: List[str]):
    query = db.query(models.Job).filter(models.Job.active == True)
    if career_id is not None:
        query = query.filter(models.Job.career_id == career_id)
    if job_type is not None:
        query = query.filter(models.Job.job_type == job_type)
    result = query.all()

    return result


def get_job_by_id(db: Session, job_id: int):
    return db.query(models.Job).filter(models.Job.id == job_id).first()


def get_jobs_by_company_id(db: Session, company_id: int):
    query = db.query(models.Job).filter(models.Job.active == True)
    company = company_services.get_company_by_id(db, company_id)

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.HTTP_EXCEPTION_401_COMPANY_DOESNT_EXIST.value,
        )

    query.filter(models.Job.company_id == company.id)
    result = query.all()
    return result


def create_job(db: Session, job: schemas.JobCreateForm, file_id: int):
    career = career_services.get_career_by_name(db, job.career)
    city = city_services.get_city_by_name(db, job.city)

    if career is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.CAREER_NOT_FOUND.value,
        )

    if city is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.CITY_NOT_FOUND.value,
        )

    today = datetime.today().date()
    job_created_at = today.strftime("%Y-%m-%d")

    if file_id is None:
        db_job = models.Job(
            description=job.description,
            job_type=job.job_type,
            active=True,
            creation_date=job_created_at,
            company_id=job.company_id,
            career_id=career.id,
            city_id=city.id,
            file_id=None,
        )
    else:
        db_job = models.Job(
            description=job.description,
            job_type=job.job_type,
            active=True,
            creation_date=job_created_at,
            company_id=job.company_id,
            career_id=career.id,
            city_id=city.id,
            file_id=file_id,
        )

    db.add(db_job)
    db.flush()
    return db_job
