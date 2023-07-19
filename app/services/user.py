import json
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
    query = db.query(models.User).all()

    for user in query:
        if user.skill is not None:
            try:
                user.skill = json.loads(user.skill)
                user.skills = user.skill
                del user.skill
            except json.JSONDecodeError:
                user.skill = None

    return query


def get_user_by_id(db: Session, user_id: int):
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user.skill is not None:
        try:
            user.skill = json.loads(user.skill)
            user.skills = user.skill
            del user.skill
        except json.JSONDecodeError:
            user.skill = None

    return user


def get_user_by_email(db: Session, email: str):
    user = (
        db.query(models.User)
        .filter(func.lower(models.User.email) == email.lower())
        .first()
    )

    if user.skill is not None:
        try:
            user.skill = json.loads(user.skill)
            user.skills = user.skill
            del user.skill
        except json.JSONDecodeError:
            user.skill = None
    return user


def skill_encoder(obj):
    if isinstance(obj, schemas.Skill):
        return obj.__dict__
    raise TypeError(f"Objeto del tipo {type(obj).__name__} no es JSON serializable")


def create_user(db: Session, user: schemas.UserCreate):
    password = user.password
    hashed_password = auth_services.get_password_hash(password)
    phone_number = user.phone_number
    career = user.career
    if phone_number:
        phone_number = phone_number.strip()
    if career:
        db_career = career_services.get_career_by_name(db, career)
        db_user = models.User(
            email=user.email.lower(),
            password=hashed_password,
            full_name=user.full_name,
            phone_number=phone_number,
            career_id=db_career.id,
            file_id=None,
        )
        db.add(db_user)
        db.flush()
    return db_user


def edit_user(db: Session, user_id: int, user: schemas.UserCreate):
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
        if user.skills is not None:
            db_user.skills = json.dumps(user.skills, default=skill_encoder)
            db_user.skill = db_user.skills
            del db_user.skills
        else:
            db_user.skill = None
            del db_user.skills

        db.flush()
        return db_user
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )


def get_password_reset_code(db: Session, user_email: str):
    db_user = get_user_by_email(db, user_email)
    if db_user:
        plain_password_code = "".join(
            secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
        )
        hashed_password = auth_services.get_password_hash(plain_password_code)
        db_user.password_reset_code = hashed_password
        db.flush()
        return {"user": db_user, "password_code": plain_password_code}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=ErrorMessage.USER_EMAIL_NOT_FOUND.value,
        )
