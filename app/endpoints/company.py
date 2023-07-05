import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import api, get_db
from ..utils.ErrorMessage import ErrorMessage
from app.schemas import company as schemas
from app.schemas import password as pass_schemas
from app.services import company as services
from app.services import auth as auth_services
from app.services import email as email_services

logger = logging.getLogger(__name__)


# @api.get("/company/me/", response_model=schemas.Company, tags=["company"])
# async def read_company_me(current_company: schemas.Company = Depends(auth_services.get_current_company)):
#     return current_company


@api.get(
    "/company/all/",
    response_model=List[schemas.Company],
    tags=["company"],
    summary="Obtener todas las empresas",
)
def get_companys(
    db: Session = Depends(get_db), token: str = Depends(auth_services.oauth2_scheme)
):
    companys = services.get_companys(db)
    return companys


@api.get(
    "/company/email/{email}/",
    response_model=schemas.Company,
    tags=["company"],
    summary="Obtener empresa por correo",
)
async def get_company_by_mail(
    email: str,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    company = services.get_company_by_email(db, email)
    logger.info(vars(company))
    return company


@api.post("/company/create/", tags=["company"], summary="Crear una empresa")
def create_company(company: schemas.CompanyCreate, db: Session = Depends(get_db)):
    try:
        db_company = services.get_company_by_email(db=db, email=company.email)
        if db_company:
            logger.info(f"db_company: {db_company}")
            raise HTTPException(
                status_code=400,
                detail=ErrorMessage.BUSINESS_INFO_USER_EMAIL_REGISTERED.value,
            )

        resp = services.create_company(db=db, company=company)
        logger.info(f"resp create company: {resp}")
        db.commit()
        return {"message": "OK"}
    except HTTPException as ex:
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value
        )


@api.post(
    "/company/recover-password/", tags=["company"], summary="Recuperar contraseña"
)
async def recover_password(
    data: pass_schemas.PasswordEmail, db: Session = Depends(get_db)
):
    try:
        company_password_code = services.get_password_reset_code(db, data.email)
        db.commit()
        name = company_password_code["company"].name
        email = company_password_code["company"].email
        password_reset_code = company_password_code["password_code"]
        return await email_services.send_password_recovery_email(
            name, email, password_reset_code
        )
    except HTTPException as ex:
        db.rollback()
        logger.exception(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        logger.exception(ErrorMessage.HTTP_EXCEPTION_404.value)
        raise HTTPException(
            status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value
        )


@api.put("/company/{company_id}/", response_model=schemas.Company, tags=["company"])
def edit_company(
    company_id: int,
    company: schemas.CompanyBase,
    db: Session = Depends(get_db),
    token: str = Depends(auth_services.oauth2_scheme),
):
    try:
        res = services.edit_company(db, company_id, company)
        db.commit()
        return res
    except HTTPException as ex:
        db.rollback()
        logging.exception(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        logging.exception(ErrorMessage.HTTP_EXCEPTION_500.value)
        raise HTTPException(
            status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value
        )
