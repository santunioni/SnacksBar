import os

import uvicorn
from fastapi import FastAPI

from .routes import router

app = FastAPI(title="Users server")
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run(
        f"{os.path.basename(__file__).split('.')[0]}:app",
        port=8000,
        reload=True,
    )
