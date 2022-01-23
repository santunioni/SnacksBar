from functools import lru_cache

import ujson
from pydantic import BaseModel
from sqlalchemy import create_engine


class APIModel(BaseModel):
    class Config:
        json_loads: ujson.loads
        json_dumps: ujson.dumps
        orm_mode = True


@lru_cache(typed=True)
def create_sqlalchemy_engine(db_url: str):
    kwargs = {}
    if db_url.startswith("sqlite:///"):
        kwargs.update(
            dict(
                connect_args={"check_same_thread": False},
                echo=True,
            )
        )
    return create_engine(db_url, **kwargs)
