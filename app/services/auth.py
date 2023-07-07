import logging as log

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.env.env import HashSettings
from app.models import career
from app.services import user as user_services
from app.services import company as company_services
from app.utils.ErrorMessage import ErrorMessage


hash_variables = HashSettings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./login")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = user_services.get_user_by_email(db, username)
    company = company_services.get_company_by_email(db, username)
    if not user and not company:
        log.info("No se encontró el estudiante o empresa")
        return False

    if not user:
        if not verify_password(password, company.password) and not verify_password(
            password, company.password_reset_code
        ):
            log.info(
                f"Comparar contraseñas empresa: {verify_password(password, company.password)}"
            )
            return False

        del (
            company.password,
            company.password_reset_code,
        )

        return {"company": company}

    if not company:
        if not verify_password(password, user.password) and not verify_password(
            password, user.password_reset_code
        ):
            log.info(
                f"Comparar contraseñas estudiante: {verify_password(password, user.password)}"
            )
            return False

        user.career_name = user.career.name

        del (
            user.career,
            user.career_id,
            user.file,
            user.file_id,
            user.password,
            user.password_reset_code,
        )

        return {"user": user}


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode, hash_variables.SECRET_KEY, algorithm=hash_variables.ALGORITHM
    )
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorMessage.HTTP_EXCEPTION_401.value,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, hash_variables.SECRET_KEY, algorithms=[hash_variables.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data_user = username
    except JWTError:
        raise credentials_exception

    return token_data_user


async def get_current_company(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=ErrorMessage.HTTP_EXCEPTION_401.value,
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, hash_variables.SECRET_KEY, algorithms=[hash_variables.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data_company = username
    except JWTError:
        raise credentials_exception

    return token_data_company
