import secrets
import string
import logging

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import user as models
from app.schemas import user as schemas
from app.services import auth as auth_services
from app.services import career as career_services
from app.utils.ErrorMessage import ErrorMessage


logger = logging.getLogger(__name__)


def get_users(db: Session):
    return db.query(models.User).all()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(func.lower(models.User.email) == email.lower()).first()


def create_user(db: Session, user: schemas.UserCreate):
    logger.info(user)
    password = user.password
    hashed_password = auth_services.get_password_hash(password)
    phone_number = user.phone_number
    career = user.career
    if phone_number:
        logger.info("Entre al if de phone number")
        phone_number = phone_number.strip()
    if career:
        logger.info("Entre al if de career")
        db_career = career_services.get_career_by_name(db, career)
        logger.info(db_career.name)
        db_user = models.User(email=user.email.lower(), password=hashed_password,
                              full_name=user.full_name, phone_number=phone_number, 
                              career_id=db_career.id)
        logger.info(db_user.email)
        db.add(db_user)
        db.flush()
    return db_user


def edit_user(db: Session, user_id: int, user: schemas.UserEdit):
    try:
        phone_number = user.phone_number
        career = user.career
        if phone_number:
            phone_number = phone_number.strip()
        if career:
            career_id = career_services.get_career_by_name(db, career).id
        db_user = get_user_by_id(db, user_id)
        db_user.email = user.email
        db_user.full_name = user.full_name
        db_user.phone_number = phone_number
        db_user.career_id = career_id
        db.flush()
        return db_user
    except Exception:
        raise HTTPException(status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value)


def get_password_reset_code(db: Session, user_email: str):
    db_user = get_user_by_email(db, user_email)
    if (db_user):
        plain_password_code = ''.join(secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16))
        hashed_password = auth_services.get_password_hash(plain_password_code)
        db_user.password_reset_code = hashed_password
        db.flush()
        return {'user': db_user, 'password_code': plain_password_code}
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="El correo ingresado no se encuentra registrado.")