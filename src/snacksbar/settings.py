from functools import lru_cache

from pydantic import BaseSettings


class APISettings(BaseSettings):
    PRODUCTS_DB_URL: str = "sqlite:///databases/products.sqlite3"
    CACHE_DB_URL: str = "redis://localhost:6379/0"
    OAUTH_TOKEN_URL: str = "auth/token"

    @classmethod
    @lru_cache()
    def from_cache(cls):
        return cls()
