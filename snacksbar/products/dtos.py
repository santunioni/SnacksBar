from decimal import Decimal
from typing import Sequence

from pydantic import Field

from snacksbar.utils import APIModel


class PricedIn(APIModel):
    name: str
    price: Decimal


class PricedOut(PricedIn):
    id: int


class CategoryIn(PricedIn):
    ...


class CategoryOut(PricedOut):
    ...


class IngredientIn(PricedIn):
    ...


class IngredientOut(PricedOut):
    ...


class DrinkIn(PricedIn):
    ...


class DrinkOut(PricedOut):
    ...


class SnackIn(APIModel):
    name: str
    category: int = Field(..., alias="category_id")
    ingredients: Sequence[int] = Field(default_factory=list)


class SnackOut(SnackIn):
    id: int
