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
