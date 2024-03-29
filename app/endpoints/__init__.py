import logging

from fastapi import APIRouter
from app.db.database import SessionLocal


api = APIRouter()
logger = logging.getLogger(__name__)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from .auth import login
from .user import get_users
from .company import get_companys
from .job import get_jobs
from .file import upload_file
from .career import get_careers
from .city import get_cities
