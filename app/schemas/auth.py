from enum import Enum
from pydantic import BaseModel
from app.schemas.company import Company
from app.schemas.user import User


class Auth(BaseModel):
    user: User
    access_token: str
    token_type: str


class AuthCompany(BaseModel):
    company: Company
    access_token: str
    token_type: str

    class Config:
        orm_mode: True


class UserType(str, Enum):
    user = "user"
    company = "company"
