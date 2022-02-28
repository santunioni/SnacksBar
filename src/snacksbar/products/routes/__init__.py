from fastapi import APIRouter

from snacksbar.security import Scopes

from ..db.models import Category, Drink, Ingredient
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

router = APIRouter(dependencies=[Scopes.READ_PRODUCTS])
router.include_router(snacks_router)

ProductsCRUD(
    names=Names("category", "categories"),
    db_cls=Category,
    product_in=CategoryIn,
    product_out=CategoryOut,
).attach_to(router)

ProductsCRUD(
    names=Names("drink", "drinks"),
    db_cls=Drink,
    product_in=DrinkIn,
    product_out=DrinkOut,
).attach_to(router)

ProductsCRUD(
    names=Names("ingredient", "ingredients"),
    db_cls=Ingredient,
    product_in=IngredientIn,
    product_out=IngredientOut,
).attach_to(router)
