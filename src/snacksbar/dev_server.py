import uvicorn

from authserver.routes import router as auth_router
from snacksbar import create_app

app = create_app()

app.include_router(auth_router)

if __name__ == "__main__":
    uvicorn.run(
        "dev_server:app",
        host="0.0.0.0",
        port=8000,
        log_level="debug",
        workers=1,
        reload=True,
    )
