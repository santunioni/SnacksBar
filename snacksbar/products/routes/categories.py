from typing import Sequence

from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from starlette import status

from snacksbar.products.db.models import Category
from snacksbar.products.db.session import get_db
from snacksbar.products.dtos import CategoryIn, CategoryOut

router = APIRouter(prefix="/categories", tags=["categories"])


@router.get("/", response_model=Sequence[CategoryOut])
async def get_categories(session: Session = Depends(get_db)):
    return list(map(CategoryOut.from_orm, session.query(Category).all()))


@router.get("/{id}", response_model=Sequence[CategoryOut])
async def get_category(id: int, session: Session = Depends(get_db)):
    return session.query(Category).get(id)


@router.post("/", response_model=CategoryOut)
async def post_category(category: CategoryIn, session: Session = Depends(get_db)):
    category = Category(name=category.name, price=category.price)
    session.add(category)
    session.commit()
    return CategoryOut.from_orm(category)


@router.put("/{id}", response_model=CategoryOut)
async def put_category(
    id: int, category: CategoryIn, session: Session = Depends(get_db)
):
    category_db: Category = session.query(Category).get(id)
    category_db.name = category.name
    category_db.price = category.price
    session.commit()
    return CategoryOut.from_orm(category_db)


@router.delete("/{id}", status_code=204)
async def delete_category(
    id: int, response: Response, session: Session = Depends(get_db)
):
    category = session.query(Category).get(id)
    if category is None:
        response.status_code = status.HTTP_404_NOT_FOUND
        return response
    session.delete(category)
    session.commit()
