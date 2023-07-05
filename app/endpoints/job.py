import logging

from fastapi import Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional

from . import api, get_db
from ..utils.ErrorMessage import ErrorMessage
from app.schemas import job as schemas
from app.services import job as services
from app.services import auth as auth_services
from app.services import file as file_services

logger = logging.getLogger(__name__)


@api.post("/job/", tags=["job"], summary="Crear una oferta de trabajo")
async def create_job(
    job: schemas.JobCreateForm = Depends(schemas.JobCreateForm.as_form),
    db: Session = Depends(get_db),
    file: Optional[UploadFile] = File(None),
    token: str = Depends(auth_services.oauth2_scheme),
):
    logger.info(f"job to create: {job}")
    try:
        if file is None:
            logger.info(f"dentro del if file None")
            img_id = None
        else:
            logger.info(f"dentro del else file")
            if not file.content_type.endswith(
                ("image/png", "image/jpeg", "image/webp")
            ):
                raise HTTPException(
                    status_code=500,
                    detail="Formato de imagen no admitido. Formatos admitidos: PNG/JPEG/WEBP",
                )
            logger.info(f"antes del upload file")
            img_id = await file_services.upload_file(file, db)

        logger.info(f"despues del upload file y antes del create job")
        resp = services.create_job(db=db, job=job, file_id=img_id)
        logger.info(f"resp create job: {resp}")
        db.commit()
        return {"message": "OK"}
    except HTTPException as ex:
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value
        )
