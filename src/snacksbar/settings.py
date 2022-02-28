from functools import lru_cache

from pydantic import BaseSettings, Field

from global_utils import SQLiteDBMaker


class APISettings(BaseSettings):
    SNACKSBAR_DB_URL: str = Field(default_factory=SQLiteDBMaker("snacksbar"))
    CACHE_DB_URL: str = "redis://localhost:6379/0"
    OAUTH_TOKEN_URL: str = "auth/token"

    @classmethod
    @lru_cache()
    def from_cache(cls):
        return cls()
