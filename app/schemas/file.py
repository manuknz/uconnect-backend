from pydantic import BaseModel


class FileCreate(BaseModel):
    content_type: str
    file_name: str
    file_data: bytes

    class Config:
        orm_mode: True


class FileResponse(BaseModel):
    file_id: int
    content_type: str

    class Config:
        orm_mode: True


class File(FileCreate):
    id: int

    class Config:
        orm_mode: True
