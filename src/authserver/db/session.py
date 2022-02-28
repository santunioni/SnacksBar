from functools import lru_cache

from sqlalchemy.orm import Session, sessionmaker

from authserver.settings import APISettings
from global_utils import create_sqlalchemy_engine


@lru_cache(1)
def get_session_maker() -> sessionmaker:
    return sessionmaker(
        bind=create_sqlalchemy_engine(APISettings.from_cache().AUTHSERVER_DB_URL)
    )


def get_db() -> Session:
    maker = get_session_maker()
    with maker() as session:
        yield session
