import logging

from fastapi import HTTPException, UploadFile, status
from sqlalchemy.orm import Session
from app.models import File
from app.utils.ErrorMessage import ErrorMessage


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
    file = db.query(File).filter(File.id == file_id).first()
    if file:
        db.delete(file)
        db.commit()
        return True

    return False
