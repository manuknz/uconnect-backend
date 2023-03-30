from sqlalchemy import Column, BigInteger, String
from app.db.database import Base


class Company(Base):
    __tablename__ = "company"

    id = Column(BigInteger, primary_key=True, index=True)
    email = Column(String, unique=True)
    password = Column(String)
    name = Column(String)
    password_reset_code = Column(String, nullable=True)

    def __init__(self, email, password, name):
        self.email = email
        self.password = password
        self.name = name