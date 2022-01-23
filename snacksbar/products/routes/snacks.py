from typing import Sequence

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from snacksbar.products.db.models import Snack
from snacksbar.products.db.session import get_db
from snacksbar.products.dtos import SnackIn, SnackOut

router = APIRouter(prefix="/snacks", tags=["snacks"])


@router.get("/", response_model=Sequence[SnackOut])
async def get_snacks(session: Session = Depends(get_db)):
    return list(map(SnackOut.from_orm, session.query(Snack).all()))


@router.get("/{id}", response_model=Sequence[SnackOut])
async def get_snack(id: int, session: Session = Depends(get_db)):
    return session.query(Snack).get(id)


@router.post("/", response_model=SnackOut)
async def post_snack(snack: SnackIn, session: Session = Depends(get_db)):
    snack = Snack(name=snack.name, category_id=snack.category)
    session.add(snack)
    session.commit()
    return SnackOut.from_orm(snack)


@router.put("/{id}", response_model=SnackOut)
async def put_snack(id: int, snack: SnackIn, session: Session = Depends(get_db)):
    snack_db: Snack = session.query(Snack).get(id)
    snack_db.name = snack.name
    snack_db.category_id = snack.category
    session.commit()
    return SnackOut.from_orm(snack_db)


@router.delete("/{id}", status_code=204)
async def delete_snack(id: int, response: Response, session: Session = Depends(get_db)):
    snack = session.query(Snack).get(id)
    if snack is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    session.delete(snack)
    session.commit()
