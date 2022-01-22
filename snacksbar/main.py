import uvicorn
from fastapi import FastAPI

from snacksbar import products
from snacksbar.products.db import get_engine
from snacksbar.products.models import Base

app = FastAPI()
app.include_router(products.router)


@app.on_event("startup")
def migrate():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    uvicorn.run(app)
