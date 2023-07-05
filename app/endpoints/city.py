import logging

from . import api
from fastapi import Depends
from app.endpoints import get_db

from sqlalchemy.orm import Session
from app.models.city import City
from app.schemas import city as schemas
from app.services import city as services, auth


logger = logging.getLogger(__name__)


@api.get("/city/all/", tags=["city"], summary="Obtener todas las ciudades")
def get_cities(db: Session = Depends(get_db)):
    cities = db.query(City).all()
    return cities


@api.get("/city/id/{city_id}/", tags=["city"], summary="Obtener ciudad por ID")
def get_city_by_id(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_city = services.get_city_by_id(db, city_id)
    if db_city:
        return db_city


@api.get("/city/name/{city_name}/", tags=["city"], summary="Obtener ciudad por nombre")
def get_city_by_name(
    city_name: str,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_city = services.get_city_by_name(db, city_name)
    if db_city:
        return db_city


@api.post("/city/", tags=["city"], summary="Agregar ciudad")
def add_city(
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_city = City(name=city.name)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


@api.put("/city/{city_id}", tags=["city"], summary="Editar ciudad")
def edit_city(
    city_id: int,
    city: schemas.CityCreate,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_city = services.get_city_by_id(db, city_id)
    if db_city:
        db_city.name = city.name
        db.flush()
        db.commit()
        db.refresh(db_city)
        return db_city


@api.delete("/city/{city_id}", tags=["city"], summary="Eliminar ciudad")
def delete_city(
    city_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(auth.oauth2_scheme),
):
    db_city = services.get_city_by_id(db, city_id)
    if db_city:
        db.delete(db_city)
        db.flush()
        db.commit()
        return db_city
