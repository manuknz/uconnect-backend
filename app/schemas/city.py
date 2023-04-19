from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str

    class Config:
        orm_mode: True


class City(CityCreate):
    id: int

    class Config:
        orm_mode: True
