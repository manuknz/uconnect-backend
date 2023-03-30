from pydantic import BaseModel


class Career(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode: True


class CareerCreate(BaseModel):
    name: str

    class Config:
        orm_mode: True
