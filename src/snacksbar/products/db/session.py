from functools import lru_cache

from fastapi import Depends
from sqlalchemy.orm import Session, sessionmaker

from global_utils import create_sqlalchemy_engine
from snacksbar.settings import APISettings


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    return sessionmaker(
        bind=create_sqlalchemy_engine(APISettings.from_cache().SNACKSBAR_DB_URL)
    )


def get_db() -> Session:
    maker = get_session_maker()
    with maker() as session:
        yield session


DependsSession: Session = Depends(get_db)
