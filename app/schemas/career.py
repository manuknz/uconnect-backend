from pydantic import BaseModel


class CareerCreate(BaseModel):
    name: str

    class Config:
        orm_mode: True


class Career(CareerCreate):
    id: int

    class Config:
        orm_mode: True
