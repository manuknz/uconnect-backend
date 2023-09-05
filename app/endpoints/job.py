import logging

from fastapi import Depends, HTTPException, UploadFile, File, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from . import api, get_db
from ..utils.ErrorMessage import ErrorMessage
from app.schemas import job as schemas
from app.services import email_services, job as services
from app.services import auth as auth_services
from app.services import file as file_services

logger = logging.getLogger(__name__)


@api.get(
    "/job/all/",
    response_model=List[schemas.JobResponse],
    tags=["job"],
    summary="Obtener todas las ofertas de trabajo, con filtros disponibles",
)
def get_jobs(
    career_id: int = Query(None),
    job_type: str = Query(None),
    skills: Optional[List[str]] = Query(None),
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    jobs = services.get_jobs(db, career_id, job_type, skills)
    return jobs


@api.get(
    "/job/id/{job_id}/",
    response_model=schemas.JobResponse,
    tags=["job"],
    summary="Obtener oferta de trabajo por ID",
)
def get_job_by_id(
    job_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    db_job = services.get_job_by_id(db, job_id)
    if db_job:
        return db_job


@api.get(
    "/job/company-id/{company_id}/",
    response_model=List[schemas.JobResponse],
    tags=["job"],
    summary="Obtener ofertas de trabajo por ID de empresa",
)
def get_job_by_id(
    company_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    jobs = services.get_jobs_by_company_id(db, company_id)
    return jobs


@api.post(
    "/job/create/", tags=["job"], summary="Crear una oferta de trabajo, sin imagen"
)
async def create_job_without_image(
    job: schemas.JobCreateWithoutImage,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        resp = services.create_job_without_file(db=db, job=job)
        db.commit()

        db_job = services.get_job_by_id(db, resp.id)
        if db_job:
            return db_job
    except HTTPException as ex:
        logger.exception(ex)
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        logger.exception(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


@api.post("/job/apply/", tags=["job"], summary="Aplicar a una oferta de trabajo")
async def apply_to_job_offer(
    job_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        user = await auth_services.get_current_user(token)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Usuario no autorizado",
            )

        resp = services.apply_job(db=db, job_id=job_id, user=user)

        if resp is not None:
            email_sent = await email_services.send_user_job_applied_email(
                resp["company_name"],
                resp["user_name"],
                resp["career_name"],
                resp["job_date"],
                resp["email"],
            )

        if email_sent:
            db.commit()
            return {"message": "OK"}
        else:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=ErrorMessage.HTTP_EXCEPTION_500.value,
            )

    except HTTPException as ex:
        logger.exception(ex)
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        logger.exception(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


@api.put(
    "/job/{job_id}/",
    tags=["job"],
    summary="Editar oferta de trabajo",
)
async def edit_job(
    job_id: int,
    job: schemas.JobEdit,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        services.edit_job(db, job_id, job)
        db.commit()
        return {"message": "OK"}

    except HTTPException as ex:
        logger.exception(ex)
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        logger.exception(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


@api.delete(
    "/job/{job_id}/",
    tags=["job"],
    summary="Eliminar oferta de trabajo",
)
def delete_user(
    job_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        res = services.delete_job(db, job_id)
        db.commit()
        return res
    except HTTPException as ex:
        db.rollback()
        logging.exception(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        logging.exception(ErrorMessage.HTTP_EXCEPTION_500.value)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )
