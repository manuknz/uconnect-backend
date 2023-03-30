from pydantic import BaseModel


class UserBase(BaseModel):
    email: str
    full_name: str
    phone_number: str

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    password: str
    career: str


class UserEdit(UserBase):
    career: str


class User(UserBase):
    id: int
    career_id: int

    class Config:
        orm_mode = True
