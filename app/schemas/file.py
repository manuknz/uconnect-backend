from pydantic import BaseModel


class FileCreate(BaseModel):
    content_type: str
    file_name: str
    file_data: bytes

    class Config:
        orm_mode: True


class File(FileCreate):
    id: int

    class Config:
        orm_mode: True