from typing import Sequence, Optional

from fastapi import APIRouter, Path
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException
from starlette.responses import Response

from snacksbar.security import Scopes
from .dtos import SnackIn, SnackOut, SnackOutMinimal
from ..db.models import Snack
from ..db.session import DependsSession

router = APIRouter(prefix="/snacks", tags=["snacks"])

ID_PATH = Path(..., alias="id")


def _get_from_db(_id: int, session: Session) -> Optional[Snack]:
    return session.query(Snack).get(_id)


@router.get("/", response_model=Sequence[SnackOutMinimal])
async def get_snacks(session=DependsSession):
    return list(map(SnackOutMinimal.from_orm, session.query(Snack).all()))


@router.get("/{id}", response_model=SnackOut)
async def get_snack_by_id(_id=ID_PATH, session=DependsSession):
    snack = _get_from_db(_id, session)
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
    snack_db = Snack(name=snack.name, category_id=snack.category.id)

    for ingredient in snack.ingredients:
        snack_db.insert_ingredient(ingredient)

    session.add(snack_db)
    session.commit()
    return snack_db


@router.put(
    "/{id}",
    status_code=status.HTTP_200_OK,
    response_model=SnackOut,
    dependencies=[Scopes.CHANGE_PRODUCTS],
)
async def put_snack(
    snack: SnackIn,
    response: Response,
    _id=ID_PATH,
    session=DependsSession,
):
    snack_db = _get_from_db(_id, session)

    if snack_db is None:
        snack_db = Snack(id=_id, name=snack.name, category_id=snack.category.id)
        response.status_code = status.HTTP_201_CREATED
    else:
        snack_db.name = snack.name
        snack_db.category_id = snack.category.id

    for ingredient in snack.ingredients:
        snack_db.insert_ingredient(ingredient)

    session.add(snack_db)
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
