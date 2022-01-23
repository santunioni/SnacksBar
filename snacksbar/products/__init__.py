from fastapi import APIRouter

from .db.models import Base
from .db.session import get_engine
from .routes import categories, drinks, ingredients, snacks

router = APIRouter(prefix="/products")
router.include_router(categories.router)
router.include_router(snacks.router)
router.include_router(drinks.router)
router.include_router(ingredients.router)


@router.on_event("startup")
def migrate():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
