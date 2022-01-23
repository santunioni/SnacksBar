import os
from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from snacksbar.utils import create_sqlalchemy_engine


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    return sessionmaker(
        bind=create_sqlalchemy_engine(
            os.environ.get("AUTH_DB_URL", "sqlite:///databases/auth.sqlite3")
        )
    )


def get_db() -> Session:
    maker = get_session_maker()
    with maker() as session:
        yield session
