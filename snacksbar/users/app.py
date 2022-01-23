from fastapi import FastAPI

from .routes import router

app = FastAPI(title="Users server")
app.include_router(router)
