from sqlalchemy import Column, BigInteger, String, LargeBinary
from app.db.database import Base


class File(Base):
    __tablename__ = "file"

    id = Column(BigInteger, primary_key=True)
    content_type = Column(String)
    file_name = Column(String)
    file_data = Column(LargeBinary)

    def __init__(self, content_type, file_name, file_data):
        self.content_type = content_type
        self.file_name = file_name
        self.file_data = file_data
