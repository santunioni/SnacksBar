from decimal import Decimal
from typing import Sequence

import ujson
from pydantic import BaseModel, Field


class FastModel(BaseModel):
    class Config:
        json_loads: ujson.loads
        json_dumps: ujson.dumps
        orm_mode = True


class PricedIn(FastModel):
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


class SnackIn(FastModel):
    name: str
    category: int = Field(..., alias="category_id")
    ingredients: Sequence[int] = Field(default_factory=list)


class SnackOut(SnackIn):
    id: int
