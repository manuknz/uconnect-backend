import secrets
import string
import logging

from fastapi import HTTPException, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models import company as models
from app.schemas import company as schemas
from app.services import auth as auth_services
from app.utils.ErrorMessage import ErrorMessage


logger = logging.getLogger(__name__)


def get_companys(db: Session):
    return db.query(models.Company).all()


def get_company_by_id(db: Session, company_id: int):
    return db.query(models.Company).filter(models.Company.id == company_id).first()


def get_company_by_email(db: Session, email: str):
    return (
        db.query(models.Company)
        .filter(func.lower(models.Company.email) == email.lower())
        .first()
    )


def create_company(db: Session, company: schemas.CompanyCreate):
    logger.info(company)
    password = company.password
    hashed_password = auth_services.get_password_hash(password)
    db_company = models.Company(
        email=company.email.lower(), password=hashed_password, name=company.name
    )
    logger.info(db_company)
    db.add(db_company)
    db.flush()
    return db_company


def edit_company(db: Session, company_id: int, company: schemas.CompanyBase):
    try:
        db_company = get_company_by_id(db, company_id)
        db_company.email = company.email
        db_company.name = company.name
        logger.info(f"empresa: {vars(db_company)}")
        db.flush()
        return db_company
    except Exception:
        raise HTTPException(
            status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value
        )


def get_password_reset_code(db: Session, company_email: str):
    db_company = get_company_by_email(db, company_email)
    if db_company:
        plain_password_code = "".join(
            secrets.choice(string.ascii_uppercase + string.digits) for _ in range(16)
        )
        hashed_password = auth_services.get_password_hash(plain_password_code)
        db_company.password_reset_code = hashed_password
        db.flush()
        return {"company": db_company, "password_code": plain_password_code}
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El correo ingresado no se encuentra registrado.",
        )
