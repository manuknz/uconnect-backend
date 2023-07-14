import logging

from . import api
from fastapi import Depends
from app.endpoints import get_db

from sqlalchemy.orm import Session
from app.models.career import Career
from app.schemas import career as schemas
from app.services import career as services, auth


logger = logging.getLogger(__name__)


@api.get("/career/all/", tags=["career"], summary="Obtener todas las carreras")
def get_careers(db: Session = Depends(get_db)):
    careers = db.query(Career).all()
    return careers


@api.get("/career/id/{career_id}/", tags=["career"], summary="Obtener carrera por ID")
def get_career_by_id(
    career_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_career = services.get_career_by_id(db, career_id)
    if db_career:
        return db_career


@api.get(
    "/career/name/{career_name}/", tags=["career"], summary="Obtener carrera por nombre"
)
def get_career_by_name(
    career_name: str,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_career = services.get_career_by_name(db, career_name)
    if db_career:
        return db_career


@api.post(
    "/career/",
    tags=["career"],
    summary="Agregar carrera",
    description="Método utilizado para agregar carreras universitarias",
)
def add_career(
    career: schemas.CareerCreate,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_career = Career(name=career.name)
    db.add(db_career)
    db.commit()
    db.refresh(db_career)
    return db_career


@api.put("/career/{career_id}/", tags=["career"], summary="Editar carrera")
def edit_career(
    career_id: int,
    career: schemas.CareerCreate,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_career = services.get_career_by_id(db, career_id)
    if db_career:
        db_career.name = career.name
        db.flush()
        db.commit()
        db.refresh(db_career)
        return db_career


@api.delete("/career/{career_id}/", tags=["career"], summary="Eliminar carrera")
def delete_career(
    career_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_career = services.get_career_by_id(db, career_id)
    if db_career:
        db.delete(db_career)
        db.flush()
        db.commit()
        return db_career
