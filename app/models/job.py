from sqlalchemy import (
    JSON,
    Boolean,
    Column,
    Date,
    ForeignKey,
    Integer,
    BigInteger,
    String,
)
from app.db.database import Base
from sqlalchemy.orm import relationship


from .company import Company
from .career import Career
from .city import City
from .file import File


class Job(Base):
    __tablename__ = "job"

    id = Column(BigInteger, primary_key=True, index=True)
    description = Column(String)
    job_type = Column(String)
    active = Column(Boolean)
    creation_date = Column(Date)
    company_id = Column(Integer, ForeignKey("company.id"))
    career_id = Column(Integer, ForeignKey("career.id"))
    city_id = Column(Integer, ForeignKey("city.id"))
    file_id = Column(Integer, ForeignKey("file.id"), nullable=True)
    skill = Column(JSON, nullable=True)
    user = Column(JSON, nullable=True)

    company = relationship(Company, lazy="joined")
    career = relationship(Career, lazy="joined")
    city = relationship(City, lazy="joined")
    file = relationship(File, lazy="joined")

    def __init__(
        self,
        description,
        job_type,
        active,
        creation_date,
        company_id,
        career_id,
        city_id,
        file_id,
        skill=None,
        user=None,
    ):
        self.description = description
        self.job_type = job_type
        self.active = active
        self.creation_date = creation_date
        self.company_id = company_id
        self.career_id = career_id
        self.city_id = city_id
        self.file_id = file_id
        self.skill = skill
        self.user = user
