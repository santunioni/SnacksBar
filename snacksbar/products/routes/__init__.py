from fastapi import APIRouter

from ..db.models import Base, Category, Drink, Ingredient
from ..db.session import get_engine
from .dtos import (
    CategoryIn,
    CategoryOut,
    DrinkIn,
    DrinkOut,
    IngredientIn,
    IngredientOut,
)
from .priced import Names, ProductsCRUD
from .roles import read_products
from .snacks import router as snacks_router

router = APIRouter(dependencies=[read_products])
router.include_router(snacks_router)
router.include_router(
    ProductsCRUD(
        Names("category", "categories"), Category, CategoryIn, CategoryOut
    ).get_router()
)
router.include_router(
    ProductsCRUD(Names("drink", "drinks"), Drink, DrinkIn, DrinkOut).get_router()
)
router.include_router(
    ProductsCRUD(
        Names("ingredient", "ingredients"), Ingredient, IngredientIn, IngredientOut
    ).get_router()
)


@router.on_event("startup")
def migrate():
    engine = get_engine()
    Base.metadata.create_all(bind=engine)
