from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from .routes import router


def create_app() -> FastAPI:
    api = FastAPI(title="Authorization server")
    api.include_router(router)

    origins = ["*"]

    api.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    return api


app = create_app()
