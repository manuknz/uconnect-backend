from typing import List, Optional
from pydantic import BaseModel

from app.schemas.job import Skill


class UserBase(BaseModel):
    email: str
    full_name: str
    phone_number: str
    skills: Optional[List[Skill]]

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    career: str


class UserEdit(UserBase):
    career: str


class UserPassword(BaseModel):
    old_password: str
    new_password: str


class UserCv(UserCreate):
    file_id: int


class User(UserBase):
    id: int
    career_id: int
    file_id: int = None

    class Config:
        orm_mode = True
