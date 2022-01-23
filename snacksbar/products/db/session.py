import os
from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from snacksbar.utils import create_sqlalchemy_engine


@lru_cache(1)
def get_engine():
    return create_sqlalchemy_engine(
        os.environ.get("PRODUCTS_DB_URL", "sqlite:///databases/products.sqlite3")
    )


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    return sessionmaker(bind=get_engine())


def get_db() -> Session:
    maker = get_session_maker()
    with maker() as session:
        yield session
