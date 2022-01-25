from typing import Optional

import uvicorn
from fastapi import Depends, FastAPI
from throttled.fastapi import (
    HostBasedLimiter,
    TotalLimiter,
    split_dependencies_and_middlewares,
)
from throttled.limiter import Limiter
from throttled.models import Rate
from throttled.strategy import FixedWindowStrategy

from snacksbar.authserver.routes import router as auth_router
from snacksbar.products.routes import router as products_router
from snacksbar.users.dependencies import get_current_user
from snacksbar.users.dtos import UserID
from snacksbar.users.routes import router as users_router


class UserLimiter(Limiter):
    """Client specific limiter"""

    def __call__(self, user: Optional[UserID] = Depends(get_current_user)):
        self.limit(key=f"username={user.username}")


dependencies, middlewares = split_dependencies_and_middlewares(
    TotalLimiter(strategy=FixedWindowStrategy(limit=Rate(2000, 1))),
    HostBasedLimiter(strategy=FixedWindowStrategy(limit=Rate(10, 1))),
    UserLimiter(strategy=FixedWindowStrategy(limit=Rate(2, 5))),
)

app = FastAPI(title="Snacks bar", dependencies=dependencies)
app.include_router(products_router, prefix="/products")
app.include_router(users_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")
map(app.add_middleware, middlewares)


if __name__ == "__main__":
    uvicorn.run(app, workers=1)
