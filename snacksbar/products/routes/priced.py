from typing import NamedTuple, Sequence, Type

from fastapi import APIRouter, Depends, Path, Response
from sqlalchemy.orm import Session
from starlette import status

from ..db.models import Base
from ..db.session import get_db
from .dtos import PricedIn, PricedOut
from .roles import modify_products


class Names(NamedTuple):
    singular: str
    plural: str


class ProductsCRUD:
    def __init__(
        self,
        names: Names,
        db_cls: Type[Base],
        product_in: Type[PricedIn],
        product_out: Type[PricedOut],
    ):
        self.__names = names
        self.__db_cls = db_cls
        self.__product_in = product_in
        self.__product_out = product_out

    async def __get_products(self, session: Session = Depends(get_db)):
        return list(
            map(self.__product_out.from_orm, session.query(self.__db_cls).all())
        )

    async def __get_product(
        self, _id: int = Path(..., alias="id"), session: Session = Depends(get_db)
    ):
        return session.query(self.__db_cls).get(_id)

    async def __post_product(
        self, product: PricedIn, session: Session = Depends(get_db)
    ):
        drink = self.__db_cls(name=product.name, price=product.price)
        session.add(drink)
        session.commit()
        return self.__product_out.from_orm(drink)

    async def __put_product(
        self,
        product: PricedIn,
        _id: int = Path(..., alias="id"),
        session: Session = Depends(get_db),
    ):
        drink_db = session.query(self.__db_cls).get(_id)
        drink_db.name = product.name
        drink_db.price = product.price
        session.commit()
        return self.__product_out.from_orm(drink_db)

    async def __delete_product(
        self,
        response: Response,
        _id: int = Path(..., alias="id"),
        session: Session = Depends(get_db),
    ):
        drink = session.query(self.__db_cls).get(_id)
        if drink is None:
            response.status_code = status.HTTP_404_NOT_FOUND
            return response
        session.delete(drink)
        session.commit()

    def get_router(self) -> APIRouter:
        router = APIRouter(prefix=f"/{self.__names.plural}", tags=[self.__names.plural])

        router.get(
            "/",
            response_model=Sequence[self.__product_out],
            name=f"Get {self.__names.plural}",
        )(self.__get_products)

        router.get(
            "/{id}",
            response_model=Sequence[self.__product_out],
            name=f"Get {self.__names.singular} by ID",
        )(self.__get_product)

        router.post(
            "/",
            status_code=status.HTTP_201_CREATED,
            response_model=self.__product_out,
            dependencies=[modify_products],
            name=f"Post {self.__names.singular}",
        )(self.__post_product)

        router.put(
            "/{id}",
            response_model=self.__product_out,
            dependencies=[modify_products],
            name=f"Put {self.__names.singular}",
        )(self.__put_product)

        router.delete(
            "/{id}",
            status_code=status.HTTP_204_NO_CONTENT,
            dependencies=[modify_products],
            name=f"Delete {self.__names.singular}",
        )(self.__delete_product)

        return router
