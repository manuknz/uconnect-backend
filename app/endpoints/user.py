import logging

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import api, get_db
from ..utils.ErrorMessage import ErrorMessage
from app.schemas import user as schemas
from app.schemas import password as pass_schemas
from app.services import user as services
from app.services import auth as auth_services
from app.services import email as email_services

logger = logging.getLogger(__name__)


# @api.get("/users/me/", response_model=schemas.User, tags=["user"])
# async def read_users_me(current_user: schemas.User = Depends(auth_services.get_current_user)):
#     return current_user


@api.get("/users/all/", response_model=List[schemas.User], tags=["user"], summary="Obtener todos los usuarios")
def get_users(db: Session = Depends(get_db), token: str = Depends(auth_services.oauth2_scheme)):
    users = services.get_users(db)
    return users


@api.get("/users/email/{email}/", response_model=schemas.User, tags=["user"], summary="Obtener usuario por correo")
async def get_user_by_mail(email: str, db: Session = Depends(get_db), token: str = Depends(auth_services.oauth2_scheme)):
    user = services.get_user_by_email(db, email)
    logger.info(vars(user))
    return user


@api.post("/users/create/", tags=["user"], summary="Crear un usuario")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        db_user = services.get_user_by_email(db=db, email=user.email)
        logger.info(f'db_user: {db_user}')
        if (db_user):
            raise HTTPException(status_code=400, detail=ErrorMessage.BUSINESS_INFO_USER_EMAIL_REGISTERED.value)

        resp = services.create_user(db=db, user=user)
        logger.info(f'resp create user: {resp}')
        db.commit()
        return {"message": 'OK'}
    except HTTPException as ex:
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value)


@api.post("/users/recover-password/", tags=["user"], summary="Recuperar contraseña")
async def recover_password(data: pass_schemas.PasswordEmail, db: Session = Depends(get_db)):
    try:
        user_password_code = services.get_password_reset_code(db, data.email)
        db.commit()
        full_name = user_password_code['user'].full_name
        email = user_password_code['user'].email
        password_reset_code = user_password_code['password_code']
        return await email_services.send_password_recovery_email(full_name, email, password_reset_code)
    except HTTPException as ex:
        db.rollback()
        logger.exception(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        logger.exception(ErrorMessage.HTTP_EXCEPTION_404.value)
        raise HTTPException(status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value)


@api.put("/users/{user_id}/", response_model=schemas.User, tags=["user"])
def edit_user(user_id: int, user: schemas.UserEdit, db: Session = Depends(get_db), token: str = Depends(auth_services.oauth2_scheme)):
    try:
        res = services.edit_user(db, user_id, user)
        db.commit()
        return res
    except HTTPException as ex:
        db.rollback()
        logging.exception(ex.detail)
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        db.rollback()
        logging.exception(ErrorMessage.HTTP_EXCEPTION_500.value)
        raise HTTPException(status_code=500, detail=ErrorMessage.HTTP_EXCEPTION_500.value)