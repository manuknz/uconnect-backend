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


class UserCv(UserBase):
    file_id: int


class User(UserBase):
    id: int
    career_id: int
    file_id: int = None

    class Config:
        orm_mode = True
