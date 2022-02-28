from typing import Sequence

from fastapi import APIRouter, Path
from starlette import status
from starlette.exceptions import HTTPException

from snacksbar.security import Scopes

from ..db.models import Snack
from ..db.session import DependsSession
from .dtos import SnackIn, SnackOut

router = APIRouter(prefix="/snacks", tags=["snacks"])

ID_PATH: int = Path(..., alias="id")


@router.get("/", response_model=Sequence[SnackOut])
async def get_snacks(session=DependsSession):
    return list(map(SnackOut.from_orm, session.query(Snack).all()))


@router.get("/{id}", response_model=SnackOut)
async def get_snack_by_id(_id=ID_PATH, session=DependsSession):
    snack = session.query(Snack).get(_id)
    if snack is None:
        raise HTTPException(status_code=404, detail="Snack not found.")
    return snack


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=SnackOut,
    dependencies=[Scopes.CHANGE_PRODUCTS],
)
async def post_snack(snack: SnackIn, session=DependsSession):
    snack = Snack(name=snack.name, category_id=snack.category)
    session.add(snack)
    session.commit()
    return snack


@router.put("/{id}", response_model=SnackOut, dependencies=[Scopes.CHANGE_PRODUCTS])
async def put_snack(snack: SnackIn, _id=ID_PATH, session=DependsSession):
    snack_db: Snack = await get_snack_by_id(_id, session)
    snack_db.name = snack.name
    snack_db.category_id = snack.category
    session.commit()
    return snack_db


@router.delete(
    "/{id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Scopes.CHANGE_PRODUCTS],
)
async def delete_snack(
    _id=ID_PATH,
    session=DependsSession,
):
    snack_db: Snack = await get_snack_by_id(_id, session)
    session.delete(snack_db)
    session.commit()
