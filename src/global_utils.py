import pathlib
from functools import lru_cache

from sqlalchemy import create_engine


class SQLiteDBMaker:
    def __init__(self, name: str):
        self.__name = name

    def __call__(self) -> str:
        databases = (pathlib.Path(__file__).parent.parent / "data" / "sqlite").resolve()
        databases.mkdir(exist_ok=True, parents=True)
        sqlite_db = (databases / f"{self.__name}.sqlite3").resolve()
        if not sqlite_db.exists():
            sqlite_db.touch(mode=0o744, exist_ok=False)
        return f"sqlite:///{sqlite_db}"


@lru_cache(typed=True)
def create_sqlalchemy_engine(db_url: str, **kwargs):
    kwargs = kwargs.copy()
    if db_url.startswith("sqlite:///"):
        kwargs.update(
            dict(
                connect_args={"check_same_thread": False},
                echo=True,
            )
        )
    return create_engine(db_url, **kwargs)
