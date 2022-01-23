from fastapi import APIRouter

from ..db.models import Base, Category, Drink, Ingredient
from ..db.session import get_session_maker
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


ProductsCRUD(
    Names("category", "categories"), Category, CategoryIn, CategoryOut
).attach_to(router)

ProductsCRUD(Names("drink", "drinks"), Drink, DrinkIn, DrinkOut).attach_to(router)

ProductsCRUD(
    Names("ingredient", "ingredients"), Ingredient, IngredientIn, IngredientOut
).attach_to(router)


@router.on_event("startup")
def migrate():
    engine = get_session_maker().kw["bind"]
    Base.metadata.create_all(bind=engine)
