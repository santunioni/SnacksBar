from typing import Sequence

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from ..db.models import Snack
from ..db.session import get_db
from .dtos import SnackIn, SnackOut
from .roles import modify_products

router = APIRouter(prefix="/snacks", tags=["snacks"])

g_session: Session = Depends(get_db)
g_id: int = Path(..., alias="id")


@router.get("/", response_model=Sequence[SnackOut])
async def get_snacks(session=g_session):
    return list(map(SnackOut.from_orm, session.query(Snack).all()))


@router.get("/{id}", response_model=SnackOut)
async def get_snack_by_id(_id=g_id, session=g_session):
    snack = session.query(Snack).get(_id)
    if snack is None:
        raise HTTPException(status_code=404, detail="Snack not found.")
    return snack


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SnackOut,
    dependencies=[modify_products],
)
async def post_snack(snack: SnackIn, session=g_session):
    snack = Snack(name=snack.name, category_id=snack.category)
    session.add(snack)
    session.commit()
    return snack


@router.put("/{id}", response_model=SnackOut, dependencies=[modify_products])
async def put_snack(snack: SnackIn, _id=g_id, session=g_session):
    snack_db: Snack = await get_snack_by_id(_id, session)
    snack_db.name = snack.name
    snack_db.category_id = snack.category
    session.commit()
    return snack_db


@router.delete(
    "/{id}", status_code=status.HTTP_204_NO_CONTENT, dependencies=[modify_products]
)
async def delete_snack(
    _id=g_id,
    session=g_session,
):
    snack_db: Snack = await get_snack_by_id(_id, session)
    session.delete(snack_db)
    session.commit()
