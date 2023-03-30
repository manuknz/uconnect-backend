from pydantic import BaseModel


class CompanyBase(BaseModel):
    email: str
    name: str

    class Config:
        orm_mode = True


class CompanyCreate(CompanyBase):
    password: str


class Company(CompanyBase):
    id: int
    
    class Config:
        orm_mode = True