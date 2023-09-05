from datetime import datetime
import json
import logging
from typing import List, Optional
from fastapi import HTTPException, status

from sqlalchemy.orm import Session

from app.models import job as models
from app.schemas import job as schemas

from app.services import career as career_services
from app.services import city as city_services
from app.services import company as company_services
from app.services import user as user_services
from app.utils.ErrorMessage import ErrorMessage


logger = logging.getLogger(__name__)


def get_jobs(
    db: Session, career_id: int, job_type: str, skills: Optional[List[str]] = None
):
    query = db.query(models.Job).filter(models.Job.active == True)
    if career_id is not None:
        query = query.filter(models.Job.career_id == career_id)
    if job_type is not None:
        query = query.filter(models.Job.job_type == job_type)
    result = query.all()

    filtered_results = []
    for job in result:
        company = company_services.get_company_by_id(db, job.company_id)
        job.company_name = str(company.name)
        job.career_name = str(job.career.name)
        job.city_name = str(job.city.name)
        del (job.company_id, job.career, job.city)
        if job.skill is not None:
            try:
                job.skill = json.loads(job.skill)
                if skills is not None:
                    match_found = False
                    for skill in job.skill:
                        for skill_filter in skills:
                            if skill_filter == skill["skill_name"]:
                                match_found = True
                                break
                        if match_found:
                            job.skills = job.skill
                            del job.skill
                            filtered_results.append(job)
                            break
                job.skills = job.skill
                del job.skill
            except json.JSONDecodeError:
                job.skill = None
        if job.user is not None:
            try:
                job.user = json.loads(job.user)
                job.users = job.user
                del job.user
            except json.JSONDecodeError:
                job.user = None
    if filtered_results == []:
        logger.info("No se encontraron resultados con el filtro de habilidades")
        filtered_results = result

    return filtered_results


def get_job_by_id(db: Session, job_id: int, full: bool = False):
    try:
        query = db.query(models.Job).filter(models.Job.id == job_id).first()
        if query is not None:
            if not full:
                query.company_name = str(query.company.name)
                query.career_name = str(query.career.name)
                query.city_name = str(query.city.name)
                del (
                    query.career,
                    query.city,
                    query.company,
                    query.file,
                    query.company_id,
                )
            if query.skill is not None:
                try:
                    query.skill = json.loads(query.skill)
                    query.skills = query.skill
                    del query.skill
                except json.JSONDecodeError:
                    query.skill = None
            if query.user is not None:
                try:
                    query.user = json.loads(query.user)
                    query.users = query.user
                    del query.user
                except json.JSONDecodeError:
                    query.user = None
    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.JOB_NOT_FOUND.value,
        )
    return query


def get_jobs_by_company_id(db: Session, company_id: int):
    try:
        query = db.query(models.Job).filter(models.Job.active == True)
        company = company_services.get_company_by_id(db, company_id)

        if company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.HTTP_EXCEPTION_401_COMPANY_DOESNT_EXIST.value,
            )

        query.filter(models.Job.company_id == company.id)
        result = query.all()

        for job in result:
            job.company_name = str(company.name)
            job.career_name = str(job.career.name)
            job.city_name = str(job.city.name)
            del (job.company, job.career, job.city)
            if job.skill is not None:
                try:
                    job.skill = json.loads(job.skill)
                    job.skills = job.skill
                    del job.skill
                except json.JSONDecodeError:
                    job.skill = None
            if job.user is not None:
                try:
                    job.user = json.loads(job.user)
                    job.users = job.user
                    del job.user
                except json.JSONDecodeError:
                    job.user = None

    except:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.JOB_COMPANY_NOT_FOUND.value,
        )

    return result


def skill_encoder(obj):
    if isinstance(obj, schemas.Skill):
        return obj.__dict__
    raise TypeError(f"Objeto del tipo {type(obj).__name__} no es JSON serializable")


def create_job_without_file(db: Session, job: schemas.JobCreateWithoutImage):
    career = career_services.get_career_by_name(db, job.career)
    city = city_services.get_city_by_name(db, job.city)
    company = company_services.get_company_by_id(db, job.company_id)

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

    if company is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.HTTP_EXCEPTION_401_COMPANY_DOESNT_EXIST.value,
        )

    today = datetime.today().date()
    job_created_at = today.strftime("%Y-%m-%d")

    db_job = models.Job(
        description=job.description,
        job_type=job.job_type,
        active=True,
        creation_date=job_created_at,
        company_id=job.company_id,
        career_id=career.id,
        city_id=city.id,
        skill=json.dumps(job.skills, default=skill_encoder)
        if job.skills is not None
        else None,
        user=None,
        file_id=None,
    )

    db.add(db_job)
    db.flush()
    return db_job


def apply_job(db: Session, job_id: int, user: str):
    try:
        db_user = user_services.get_user_by_email(db, user)
        if db_user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.HTTP_EXCEPTION_401_USER_DOESNT_EXIST.value,
            )

        job_user = schemas.JobUser(
            email=db_user.email,
            full_name=db_user.full_name,
            phone_number=db_user.phone_number,
            career=db_user.career.name,
            file_id=db_user.file_id,
        )

        job = db.query(models.Job).filter(models.Job.id == job_id).first()
        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.JOB_NOT_FOUND.value,
            )

        db_company = company_services.get_company_by_id(db, job.company_id)
        if db_company is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.HTTP_EXCEPTION_401_COMPANY_DOESNT_EXIST.value,
            )

        db_career = career_services.get_career_by_id(db, db_user.career_id)
        if db_career is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=ErrorMessage.HTTP_EXCEPTION_401_COMPANY_DOESNT_EXIST.value,
            )

        user_list = json.loads(job.user) if job.user else []
        for user in user_list:
            if user["email"] == job_user.email:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ErrorMessage.JOB_NOT_FOUND.value,
                )

        user_list.append(job_user.dict())

        job.user = json.dumps(user_list)

        return {
            "company_name": db_company.name,
            "user_name": db_user.full_name,
            "career_name": db_career.name,
            "job_date": job.creation_date.strftime("%Y-%m-%d"),
            "email": db_company.email,
        }
    except:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


def edit_job(
    db: Session,
    job_id: int,
    job: schemas.JobEdit,
):
    try:
        career = job.career
        city = job.city
        if career:
            try:
                career_id = career_services.get_career_by_name(db, career).id
            except:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ErrorMessage.CAREER_NOT_FOUND.value,
                )
        if city:
            try:
                city_id = city_services.get_city_by_name(db, city).id
            except:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=ErrorMessage.CITY_NOT_FOUND.value,
                )
        db_job = get_job_by_id(db, job_id, True)

        db_job.description = job.description
        db_job.job_type = job.job_type
        db_job.career_id = career_id
        db_job.city_id = city_id
        if job.skills is not None:
            db_job.skills = json.dumps(job.skills, default=skill_encoder)
            db_job.skill = db_job.skills
            del db_job.skills
        else:
            db_job.skill = None
            del db_job.skills

        if db_job.users is not None:
            db_job.user = json.dumps(db_job.users)
            del db_job.users
        else:
            db_job.user = None
            del db_job.users

        db.flush()
        return db_job
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


def delete_job(db: Session, job_id: int):
    try:
        db_job = get_job_by_id(db, job_id, True)
        db_job.active = False
        db.flush()
        return {"message": ErrorMessage.INFO_GENERAL_DELETED.value}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )
