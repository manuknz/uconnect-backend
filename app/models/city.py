from sqlalchemy import Column, BigInteger, String
from app.db.database import Base


class City(Base):
    __tablename__ = "city"

    id = Column(BigInteger, primary_key=True)
    name = Column(String)

    def __init__(self, name):
        self.name = name
