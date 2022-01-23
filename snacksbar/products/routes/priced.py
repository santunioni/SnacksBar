from typing import NamedTuple, Sequence, Type

from fastapi import APIRouter, Depends, Path
from sqlalchemy.orm import Session
from starlette import status
from starlette.exceptions import HTTPException

from ..db.models import Base
from ..db.session import get_db
from .dtos import PricedIn, PricedOut
from .roles import modify_products


class Names(NamedTuple):
    singular: str
    plural: str


g_session: Session = Depends(get_db)
g_id: int = Path(..., alias="id")


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

    async def __get_products(self, session=g_session):
        return list(
            map(self.__product_out.from_orm, session.query(self.__db_cls).all())
        )

    async def __get_product_by_id(self, _id=g_id, session=g_session):
        product_db = session.query(self.__db_cls).get(_id)
        if product_db is None:
            raise HTTPException(
                status_code=404, detail=f"{self.__names.singular.title()} not found."
            )
        return product_db

    async def __post_product(self, product: PricedIn, session=g_session):
        product_db = self.__db_cls(name=product.name, price=product.price)
        session.add(product_db)
        session.commit()
        return product_db

    async def __put_product(self, product: PricedIn, _id=g_id, session=g_session):
        product_db = await self.__get_product_by_id(_id, session)
        product_db.name = product.name
        product_db.price = product.price
        session.commit()
        return product_db

    async def __delete_product(self, _id=g_id, session=g_session):
        product_db = await self.__get_product_by_id(_id, session)
        session.delete(product_db)
        session.commit()

    def attach_to(self, base_router: APIRouter):
        router = APIRouter(prefix=f"/{self.__names.plural}", tags=[self.__names.plural])

        router.get(
            "/",
            response_model=Sequence[self.__product_out],
            name=f"Get {self.__names.plural}",
        )(self.__get_products)

        router.get(
            "/{id}",
            response_model=self.__product_out,
            name=f"Get {self.__names.singular} by ID",
        )(self.__get_product_by_id)

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

        base_router.include_router(router)
