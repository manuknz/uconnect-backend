import logging

from sqlalchemy.orm import Session
from app.schemas import city as schemas
from app.models import City

logger = logging.getLogger(__name__)


def get_city_by_id(db: Session, city_id: int):
    return db.query(City).filter(City.id == city_id).first()


def get_city_by_name(db: Session, city_name: str):
    return db.query(City).filter(City.name.ilike(city_name)).first()
