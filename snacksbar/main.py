import time

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from throttled import Rate
from throttled.fastapi import APILimiter, HostBasedLimiter, TotalLimiter
from throttled.strategy import FixedWindowStrategy

from snacksbar import products

api_limiter = APILimiter()
strategy = FixedWindowStrategy(limit=Rate(1, 5))
api_limiter.append(TotalLimiter(strategy=strategy))
api_limiter.append(HostBasedLimiter(strategy=strategy))

app = FastAPI(dependencies=api_limiter.dependencies)
app.include_router(products.router)
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
