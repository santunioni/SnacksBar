import os
from functools import lru_cache
from importlib import resources
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def get_sqlite_filepath() -> str:
    with resources.path("sql", "db.sqlite3") as sqlite_filepath:
        path = f"sqlite:///{sqlite_filepath}"
        Path(sqlite_filepath).touch()
        return path


def get_engine():
    return create_engine(
        os.environ.get("DB_URL", get_sqlite_filepath()),
        connect_args={"check_same_thread": False},
    )


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    return sessionmaker(bind=get_engine())


def get_db() -> Session:
    maker = get_session_maker()
    with maker() as session:
        yield session
