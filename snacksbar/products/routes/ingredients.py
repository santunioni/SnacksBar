from typing import Sequence

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from snacksbar.products.db import get_db
from snacksbar.products.models import Ingredient
from snacksbar.products.parse import IngredientIn, IngredientOut

router = APIRouter(prefix="/ingredients", tags=["ingredients"])


@router.get("/", response_model=Sequence[IngredientOut])
async def get_ingredients(session: Session = Depends(get_db)):
    return list(map(IngredientOut.from_orm, session.query(Ingredient).all()))


@router.get("/{id}", response_model=Sequence[IngredientOut])
async def get_ingredient(id: int, session: Session = Depends(get_db)):
    return session.query(Ingredient).get(id)


@router.post("/", response_model=IngredientOut)
async def post_ingredient(ingredient: IngredientIn, session: Session = Depends(get_db)):
    ingredient = Ingredient(name=ingredient.name, price=ingredient.price)
    session.add(ingredient)
    session.commit()
    return IngredientOut.from_orm(ingredient)


@router.put("/{id}", response_model=IngredientOut)
async def put_ingredient(
    id: int, ingredient: IngredientIn, session: Session = Depends(get_db)
):
    ingredient_db: Ingredient = session.query(Ingredient).get(id)
    ingredient_db.name = ingredient.name
    ingredient_db.price = ingredient.price
    session.commit()
    return IngredientOut.from_orm(ingredient_db)


@router.delete("/{id}", status_code=204)
async def delete_ingredient(
    id: int, response: Response, session: Session = Depends(get_db)
):
    ingredient = session.query(Ingredient).get(id)
    if ingredient is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    session.delete(ingredient)
    session.commit()
