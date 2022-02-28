from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from snacksbar.settings import APISettings
from snacksbar.utils import create_sqlalchemy_engine


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    return sessionmaker(
        bind=create_sqlalchemy_engine(APISettings.from_cache().PRODUCTS_DB_URL)
    )


def get_db() -> Session:
    maker = get_session_maker()
    with maker() as session:
        yield session


DependsSession: Session = Depends(get_db)
