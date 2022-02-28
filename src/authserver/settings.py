from functools import lru_cache

from pydantic import BaseSettings


class APISettings(BaseSettings):
    AUTH_DB_URL: str = "sqlite:///databases/auth.sqlite3"

    @classmethod
    @lru_cache()
    def from_cache(cls):
        return cls()
