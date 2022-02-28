from fastapi import FastAPI

from .routes import router

app = FastAPI(title="Products server")
app.include_router(router)
