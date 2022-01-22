from functools import lru_cache
from importlib import resources
from pathlib import Path

from fastapi import Depends
from pydantic import BaseSettings, Field
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_sqlite_filepath() -> str:
    with resources.path("sql", "db.sqlite3") as sqlite_filepath:
        path = f"sqlite:///{sqlite_filepath}"
        Path(sqlite_filepath).touch()
        return path


class SQLSettings(BaseSettings):
    DB_URL: str = Field(default_factory=get_sqlite_filepath)

    def __hash__(self):
        return hash(str(self))


@lru_cache(1)
def get_engine():
    settings = SQLSettings()
    return create_engine(settings.DB_URL, connect_args={"check_same_thread": False})


@lru_cache(1)
def get_session_maker(engine=Depends(get_engine)) -> sessionmaker:
    session_maker = sessionmaker(bind=engine)
    return session_maker


def get_db(maker: sessionmaker = Depends(get_session_maker)) -> Session:
    with maker() as session:
        yield session
