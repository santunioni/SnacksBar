from typing import Optional, Sequence

from fastapi import Depends, FastAPI
from redis.client import Redis
from starlette.middleware.base import BaseHTTPMiddleware
from throttled.fastapi import (
    FastAPILimiter,
    IPLimiter,
    TotalLimiter,
    split_dependencies_and_middlewares,
)
from throttled.models import Rate
from throttled.storage.memory import MemoryStorage
from throttled.storage.redis import RedisStorage

from snacksbar.products.routes import router as products_router
from snacksbar.users.dependencies import get_current_user
from snacksbar.users.dtos import UserID
from snacksbar.users.routes import router as users_router


class UserLimiter(FastAPILimiter):
    """Client specific limiter"""

    def __call__(self, user: Optional[UserID] = Depends(get_current_user)):
        self.limit(key=f"username={user.username}")


def create_limiters() -> Sequence[FastAPILimiter]:
    memory = MemoryStorage(cache={})
    api_limiter = TotalLimiter(limit=Rate(2000, 1), storage=memory)

    redis = RedisStorage(client=Redis.from_url("redis://localhost"))
    ip_limiter = IPLimiter(limit=Rate(10, 1), storage=redis)
    user_limiter = UserLimiter(limit=Rate(2, 5), storage=redis)

    return api_limiter, ip_limiter, user_limiter


def create_app(limiters: Sequence[FastAPILimiter] = tuple()) -> FastAPI:
    dependencies, middlewares = split_dependencies_and_middlewares(*limiters)

    api = FastAPI(title="Snacks bar", dependencies=dependencies)

    api.include_router(products_router, prefix="/products")
    api.include_router(users_router, prefix="/users")

    for mid in middlewares:
        api.add_middleware(BaseHTTPMiddleware, dispatch=mid)

    return api


app = create_app(create_limiters())
