import logging

from fastapi import Depends, HTTPException, UploadFile, File, status
from sqlalchemy.orm import Session
from typing import List, Optional

from . import api, get_db
from ..utils.ErrorMessage import ErrorMessage
from app.schemas import job as schemas
from app.services import job as services
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
    career_id: int = None,
    job_type: str = None,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    jobs = services.get_jobs(db, career_id, job_type)
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


@api.post("/job/", tags=["job"], summary="Crear una oferta de trabajo")
async def create_job(
    job: schemas.JobCreateForm = Depends(schemas.JobCreateForm.as_form),
    db: Session = Depends(get_db),
    file: Optional[UploadFile] = File(None),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        if file is None:
            img_id = None
        else:
            if not file.content_type.endswith(
                ("image/png", "image/jpeg", "image/webp")
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.IMAGE_EXTENSION_NOT_ALLOWED.value,
                )
            img_id = await file_services.upload_file(file, db)

        resp = services.create_job(db=db, job=job, file_id=img_id)
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


@api.put(
    "/job/{job_id}/",
    tags=["job"],
    summary="Editar oferta de trabajo",
)
async def edit_job(
    job_id: int,
    job: schemas.JobEditForm = Depends(schemas.JobEditForm.as_form),
    db: Session = Depends(get_db),
    file: Optional[UploadFile] = File(None),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        if file is None:
            img_id = None
        else:
            if not file.content_type.endswith(
                ("image/png", "image/jpeg", "image/webp")
            ):
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.IMAGE_EXTENSION_NOT_ALLOWED.value,
                )
            img_id = await file_services.upload_file(file, db)

        try:
            res = services.edit_job(db, job_id, job, img_id)
            db.commit()
            logger.info(res)
            return {"message": "OK"}
        except HTTPException as ex:
            db.rollback()
            logging.exception(ex.detail)
            raise HTTPException(status_code=ex.status_code, detail=ex.detail)

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
    "/job/{job_id}",
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
