import time

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from throttled import Rate
from throttled.fastapi import APILimiter, HostBasedLimiter, TotalLimiter
from throttled.strategy import FixedWindowStrategy

from snacksbar.authserver.routes import router as auth_router
from snacksbar.products.routes import router as products_router
from snacksbar.users.routes import router as users_router

api_limiter = APILimiter()
strategy = FixedWindowStrategy(limit=Rate(100, 5))
api_limiter.append(TotalLimiter(strategy=strategy))
api_limiter.append(HostBasedLimiter(strategy=strategy))

app = FastAPI(title="Snacks bar", dependencies=api_limiter.dependencies)
app.include_router(products_router, prefix="/products")
app.include_router(users_router, prefix="/users")
app.include_router(auth_router, prefix="/auth")

api_limiter.inject_middlewares_in_app(app)


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


if __name__ == "__main__":
    uvicorn.run(app, workers=1)
