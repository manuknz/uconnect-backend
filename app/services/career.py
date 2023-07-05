import logging

from sqlalchemy.orm import Session
from app.schemas import career as schemas
from app.models import Career

logger = logging.getLogger(__name__)


def get_career_by_id(db: Session, career_id: int):
    return db.query(Career).filter(Career.id == career_id).first()


def get_career_by_name(db: Session, career_name: str):
    return db.query(Career).filter(Career.name.ilike(career_name)).first()
