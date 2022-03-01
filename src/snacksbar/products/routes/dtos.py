from decimal import Decimal
from typing import Sequence

from pydantic import Field

from snacksbar.utils import APIModel


class Identified(APIModel):
    id: int


class PricedIn(APIModel):
    name: str
    price: Decimal


class PricedOut(PricedIn, Identified):
    ...


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
    category: Identified
    ingredients: Sequence[Identified] = Field(default_factory=list)


class SnackOutMinimal(SnackIn, Identified):
    ...


class SnackOut(SnackIn, Identified):
    category: PricedOut
    ingredients: Sequence[PricedOut] = Field(default_factory=list)
