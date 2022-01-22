from typing import Sequence

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from snacksbar.products.db import get_db
from snacksbar.products.models import Drink
from snacksbar.products.parse import DrinkIn, DrinkOut

router = APIRouter(prefix="/drinks", tags=["drinks"])


@router.get("/", response_model=Sequence[DrinkOut])
async def get_drinks(session: Session = Depends(get_db)):
    return list(map(DrinkOut.from_orm, session.query(Drink).all()))


@router.get("/{id}", response_model=Sequence[DrinkOut])
async def get_drink(id: int, session: Session = Depends(get_db)):
    return session.query(Drink).get(id)


@router.post("/", response_model=DrinkOut)
async def post_drink(drink: DrinkIn, session: Session = Depends(get_db)):
    drink = Drink(name=drink.name, price=drink.price)
    session.add(drink)
    session.commit()
    return DrinkOut.from_orm(drink)


@router.put("/{id}", response_model=DrinkOut)
async def put_drink(id: int, drink: DrinkIn, session: Session = Depends(get_db)):
    drink_db: Drink = session.query(Drink).get(id)
    drink_db.name = drink.name
    drink_db.price = drink.price
    session.commit()
    return DrinkOut.from_orm(drink_db)


@router.delete("/{id}", status_code=204)
async def delete_drink(id: int, response: Response, session: Session = Depends(get_db)):
    drink = session.query(Drink).get(id)
    if drink is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    session.delete(drink)
    session.commit()
