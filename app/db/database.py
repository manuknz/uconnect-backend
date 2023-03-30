from sqlalchemy import create_engine
from sqlalchemy.pool import NullPool
from sqlalchemy.engine.url import URL
from sqlalchemy.engine import Engine as Database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.env.env import DBSettings

dbSettings = DBSettings()

DATABASE_URL = dbSettings.DATABASE_URL
DATABASE_USER = dbSettings.DATABASE_USER
DATABASE_PW = dbSettings.DATABASE_PW
DATABASE_DB = dbSettings.DATABASE_DB
DATABASE_DRIVER = dbSettings.DATABASE_DRIVER
DATABASE_NAME = dbSettings.DATABASE_NAME

UCONNECT_URL = f'{DATABASE_DB}://{DATABASE_USER}:{DATABASE_PW}@{DATABASE_URL}/{DATABASE_NAME}'

engine_uconnect = create_engine(UCONNECT_URL, pool_size=20, max_overflow=15)
SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine_uconnect)

Base = declarative_base()


def get_database_connection() -> Database:
    assert engine_uconnect is not None
    return engine_uconnect
