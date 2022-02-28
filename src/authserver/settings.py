from functools import lru_cache

from pydantic import BaseSettings, Field

from global_utils import SQLiteDBMaker


class APISettings(BaseSettings):
    AUTHSERVER_DB_URL: str = Field(default_factory=SQLiteDBMaker("authserver"))

    @classmethod
    @lru_cache()
    def from_cache(cls):
        return cls()
