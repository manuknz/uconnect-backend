from sqlalchemy import Column, ForeignKey, Integer, BigInteger, String
from app.db.database import Base
from sqlalchemy.orm import relationship

from .career import Career
from .file import File


class User(Base):
    __tablename__ = "user"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    full_name = Column(String)
    phone_number = Column(String)
    password_reset_code = Column(String, nullable=True)
    career_id = Column(Integer, ForeignKey("career.id"))
    file_id = Column(Integer, ForeignKey("file.id"))

    career = relationship(Career, lazy='joined')
    file = relationship(File, lazy='joined')

    def __init__(self, email, password, full_name, phone_number, career_id, file_id):
        self.email = email
        self.password = password
        self.full_name = full_name
        self.phone_number = phone_number
        self.career_id = career_id
        self.file_id = file_id
