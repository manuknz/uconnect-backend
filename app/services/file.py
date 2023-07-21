import logging

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app import models
from app.models import File
from app.utils.ErrorMessage import ErrorMessage
from app.services import user as user_services
from app.services import job as job_services


logger = logging.getLogger(__name__)


def get_files(db: Session):
    files = db.query(File.id, File.content_type).all()
    return files


def get_file_by_id(file_id: int, db: Session):
    file = db.query(File).filter(File.id == file_id).first()
    if not file:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.FILE_NOT_FOUND.value,
        )

    return file


async def upload_file(file: UploadFile, db: Session):
    try:
        file_content = await file.read()

        # Crear una instancia del modelo File con los datos del archivo
        db_file = File(
            content_type=file.content_type,
            file_name=file.filename,
            file_data=file_content,
        )

        # Guardar el archivo en la base de datos
        db.add(db_file)
        db.commit()
        db.refresh(db_file)
        return db_file.id
    except FileNotFoundError:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.FILE_NOT_FOUND.value,
        )
    except Exception as e:
        logger.error(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


def delete_file(db: Session, file_id: int):
    # Verificar si el archivo está relacionado con algún Job
    job_with_file = db.query(models.Job).filter(models.Job.file_id == file_id).first()
    if job_with_file:
        # Eliminar la relación del archivo con el Job
        job_with_file.file_id = None
        db.commit()

    # Verificar si el archivo está relacionado con algún User
    user_with_file = (
        db.query(models.User).filter(models.User.file_id == file_id).first()
    )
    if user_with_file:
        # Eliminar la relación del archivo con el User
        user_with_file.file_id = None
        db.commit()

    # Luego de eliminar las relaciones, eliminar definitivamente el archivo
    file = db.query(File).filter(File.id == file_id).first()
    if file:
        db.delete(file)
        db.commit()
        return True, "File deleted successfully."

    return False, "File not found."


def assign_file_to_user(user_id: int, file_id: int, db: Session):
    db.query(models.User).filter(models.User.id == user_id).update({"file_id": file_id})
    db.commit()
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.USER_NOT_FOUND.value,
        )
    return user


def assign_file_to_job(job_id: int, file_id: int, db: Session):
    db.query(models.Job).filter(models.Job.id == job_id).update({"file_id": file_id})
    db.commit()
    job = db.query(models.Job).filter(models.Job.id == job_id).first()
    if not job:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ErrorMessage.USER_NOT_FOUND.value,
        )
    return job
