import logging

from fastapi import Depends, HTTPException, UploadFile, File
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from . import api, get_db
from ..utils.ErrorMessage import ErrorMessage
from app.schemas import file as schemas
from app.services import file as services
from app.services import auth as auth_services

logger = logging.getLogger(__name__)


@api.get("/file/all/", tags=["file"], response_model=list[schemas.FileResponse], summary="Obtener los archivos cargados")
def get_files(db: Session = Depends(get_db)):
    files = services.get_files(db)
    
    return [schemas.FileResponse(file_id=file[0], content_type=file[1]) for file in files]


@api.get("/file/{file_id}/", tags=["file"], summary="Obtener un archivo por ID")
def get_file(file_id: int, db: Session = Depends(get_db)):
    file_id_str = file_id # Este valor es solo un ejemplo. En su caso, puede ser cualquier valor que no sea un objeto int.
    file_id_int = int(file_id_str)
    file = services.get_file_by_id(file_id_int, db)
    if file is None:
        return {"detail": "El archivo no existe"}
    
    return StreamingResponse(iter([file.file_data]), media_type=file.content_type, headers={"Content-Disposition": f"attachment;filename={file.file_name}"})


@api.post("/file/upload/", tags=["file"], summary="Cargar un archivo")
async def upload_file(file: UploadFile = File(...), db: Session = Depends(get_db), token: str = Depends(auth_services.oauth2_scheme)):
    try:
        if not file.content_type.endswith(('image/png', 'image/jpeg', 'image/webp', 'application/pdf')):
            raise HTTPException(status_code=500, detail="Formato de archivo no permitido. Formatos permitidos: PNG/JPEG/WEBP/PDF")
        db_file = await services.upload_file(file, db)
        return db_file
    except HTTPException as ex:
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value)


@api.delete("/file/delete/{file_id}/", tags=["file"], summary="Eliminar un archivo")
async def delete_file(file_id: int, db: Session = Depends(get_db)):
    if not services.delete_file(db, file_id):
        raise HTTPException(status_code=404, detail="El archivo no existe.")
    
    return {"detail": "Archivo eliminado"}