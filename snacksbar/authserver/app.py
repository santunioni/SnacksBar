from fastapi import FastAPI

from .routes import router

app = FastAPI(title="Authorization server")
app.include_router(router)
