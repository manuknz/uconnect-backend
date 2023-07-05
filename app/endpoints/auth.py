import logging

from . import api, get_db
from app.env.env import HashSettings
from app.services import auth as auth_services
from app.utils.ErrorMessage import ErrorMessage

from datetime import timedelta
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm


hash_variables = HashSettings()
logger = logging.getLogger(__name__)


@api.post("/login/", tags=["auth"], summary="Iniciar sesión")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    authenticate = auth_services.authenticate_user(
        db, form_data.username, form_data.password
    )

    if not authenticate:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=ErrorMessage.HTTP_EXCEPTION_401_INVALID_CREDENTIAL.value,
        )

    if authenticate.get("user"):
        user = authenticate.get("user")
        access_token_expires = timedelta(
            minutes=hash_variables.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = auth_services.create_access_token(
            data={"sub": user.email}, expires_delta=access_token_expires
        )
        return {"user": user, "access_token": access_token, "token_type": "bearer"}

    elif authenticate.get("company"):
        company = authenticate.get("company")
        access_token_expires = timedelta(
            minutes=hash_variables.ACCESS_TOKEN_EXPIRE_MINUTES
        )
        access_token = auth_services.create_access_token(
            data={"sub": company.email}, expires_delta=access_token_expires
        )
        return {
            "company": company,
            "access_token": access_token,
            "token_type": "bearer",
        }
