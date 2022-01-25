from fastapi import APIRouter

from snacksbar.security import Scopes

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
from .snacks import router as snacks_router

router = APIRouter(dependencies=[Scopes.READ_PRODUCTS.fastapi])
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
    if "sqlite:///" in str(engine.url):
        Base.metadata.create_all(bind=engine)
