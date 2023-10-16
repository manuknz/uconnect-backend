import logging

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from passlib.context import CryptContext
from jose import JWTError, jwt

from app.endpoints.auth import UserType
from app.env.env import HashSettings
from app.models import user as user_models
from app.models import company as company_models
from app.schemas.user import UserPassword
from app.services import user as user_services
from app.services import company as company_services
from app.utils.ErrorMessage import ErrorMessage


hash_variables = HashSettings()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="./login")


logger = logging.getLogger(__name__)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(db, username: str, password: str):
    user = user_services.get_user_by_email(db, username)
    company = company_services.get_company_by_email(db, username)
    if not user and not company:
        logger.info("No se encontró el estudiante o empresa")
        return False

    if not user:
        if not verify_password(password, company.password) and not verify_password(
            password, company.password_reset_code
        ):
            logger.info(
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
            logger.info(
                f"Comparar contraseñas estudiante: {verify_password(password, user.password)}"
            )
            return False

        user.career_name = user.career.name

        del (
            user.career,
            user.career_id,
            user.file,
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


def change_password(db: Session, id: int, type: str, user_passwords: UserPassword):
    try:
        if type == UserType.user:
            user = user_services.get_user_by_id(db, id)
            password = user.password
            password_reset_code = user.password_reset_code
            new_password = user_passwords.new_password
            old_password = user_passwords.old_password
            if not verify_password(old_password, password) and not verify_password(
                old_password, password_reset_code
            ):
                logger.info(
                    f"Comparar contraseñas: {verify_password(old_password, password)}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.USER_OLD_PASSWORD_INCORRECT.value,
                )
            new_hashed_password = get_password_hash(new_password)
            db.query(user_models.User).filter(user_models.User.id == id).update(
                {"password": new_hashed_password, "password_reset_code": None}
            )
            db.flush()
            res = user_services.get_user_by_id(db, id)
        elif type == UserType.company:
            company = company_services.get_company_by_id(db, id)
            password = company.password
            new_password = user_passwords.new_password
            old_password = user_passwords.old_password
            if not verify_password(old_password, password):
                logger.info(
                    f"Comparar contraseñas: {verify_password(old_password, password)}"
                )
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=ErrorMessage.USER_OLD_PASSWORD_INCORRECT.value,
                )
            new_hashed_password = get_password_hash(new_password)
            db.query(company_models.Company).filter(
                company_models.Company.id == id
            ).update({"password": new_hashed_password, "password_reset_code": None})
            db.flush()
            res = company_services.get_company_by_id(db, id)
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=ErrorMessage.USER_TYPE_INVALID.value,
            )
        return res
    except HTTPException as ex:
        logger.exception(ex)
        db.rollback()
        raise HTTPException(status_code=ex.status_code, detail=ex.detail)
    except Exception as e:
        logger.exception(e)
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=ErrorMessage.HTTP_EXCEPTION_500.value,
        )
