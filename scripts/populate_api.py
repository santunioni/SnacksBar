from decimal import Decimal
from typing import NamedTuple, Optional, Sequence

from devtools import debug as print
from requests import Session
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

from snacksbar.products.dtos import Identified, PricedIn, SnackIn
from snacksbar.utils import APIModel


class UpsertModel(NamedTuple):
    id: int
    model: APIModel


class Priced(PricedIn):
    price: float

    class Config:
        json_encoders = {Decimal: str}


integredients: Sequence[UpsertModel] = [
    UpsertModel(id=1, model=Priced(name="Mussarela", price=3.5)),
    UpsertModel(id=2, model=Priced(name="Cheddar", price=3.5)),
    UpsertModel(id=3, model=Priced(name="Catupiry", price=3.5)),
    UpsertModel(id=4, model=Priced(name="Bife de Hamburguer", price=4.0)),
    UpsertModel(id=5, model=Priced(name="Filé de Frango", price=5.0)),
    UpsertModel(id=6, model=Priced(name="Ovo", price=1.5)),
    UpsertModel(id=7, model=Priced(name="Presunto", price=2.5)),
    UpsertModel(id=8, model=Priced(name="Calabresa", price=2.5)),
    UpsertModel(id=9, model=Priced(name="Bacon", price=3.5)),
    UpsertModel(id=10, model=Priced(name="Pão", price=0.0)),
    UpsertModel(id=11, model=Priced(name="Salada", price=0.0)),
]

categories: Sequence[UpsertModel] = [
    UpsertModel(id=1, model=Priced(name="Carne de Boi", price=8.5)),
    UpsertModel(id=2, model=Priced(name="Filé de Frango", price=10.00)),
    UpsertModel(id=3, model=Priced(name="Carne de Boi e Frango", price=14.0)),
    UpsertModel(id=4, model=Priced(name="Carne de Boi com Presunto", price=11.0)),
    UpsertModel(id=5, model=Priced(name="Filé de Frango com Presunto", price=12.5)),
    UpsertModel(id=6, model=Priced(name="Misto quente", price=8.5)),
    UpsertModel(id=7, model=Priced(name="Carne de boi com calabresa", price=11.0)),
    UpsertModel(id=8, model=Priced(name="Lanches Especiais", price=19.5)),
]


def id_list_to_dict(id_list: Sequence[int]) -> list[Identified]:
    return [Identified(id=_id) for _id in id_list]


snacks: Sequence[UpsertModel] = [
    UpsertModel(
        id=1,
        model=SnackIn(
            name="Hamburguer",
            category={"id": 1},
            ingredients=id_list_to_dict((10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=2,
        model=SnackIn(
            name="Cheese Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((1, 10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=3,
        model=SnackIn(
            name="Cheese Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((6, 10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=4,
        model=SnackIn(
            name="Cheese Egg Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((1, 6, 10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=5,
        model=SnackIn(
            name="Bacon Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((9, 10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=6,
        model=SnackIn(
            name="Cheese Bacon Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((1, 9, 10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=7,
        model=SnackIn(
            name="Egg Bacon Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((6, 9, 10, 4, 11)),
        ),
    ),
    UpsertModel(
        id=8,
        model=SnackIn(
            name="Cheese Egg Bacon Burguer",
            category={"id": 1},
            ingredients=id_list_to_dict((1, 6, 9, 10, 4, 11)),
        ),
    ),
]


def populate(
    session: Optional[Session] = None, api_url: str = "http://localhost:8001/products"
):
    if session is None:
        session = Session()
    for ingredient in integredients:
        print(
            session.put(
                f"{api_url}/ingredients/{ingredient.id}", json=ingredient.model.dict()
            )
        )
    for category in categories:
        print(
            session.put(
                f"{api_url}/categories/{category.id}", json=category.model.dict()
            )
        )
    for snack in snacks:
        print(session.put(f"{api_url}/snacks/{snack.id}", json=snack.model.dict()))
    session.close()


def fetch_token(token_url: str = "https://localhost:8000/token") -> str:
    scope = ["me", "products:read", "products:modify"]
    oauth = OAuth2Session(scope=scope)
    token = oauth.fetch_token(
        token_url,
        auth=HTTPBasicAuth(
            username="johndoe",
            password="secret",
        ),
    )
    return token


def create_session(token: str) -> Session:
    session = Session()
    session.headers["Authorization"] = f"Bearer {token}"
    return session


TOKEN = (
    "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJqb2huZG9lIiwic2NvcGVzIjpbInByb2R1Y3"
    "RzOm1vZGlmeSIsInByb2R1Y3RzOnJlYWQiLCJtZSJdLCJleHAiOjE2NDY1MjQ0MzksImVtYWlsIjoiam9ob"
    "mRvZUBleGFtcGxlLmNvbSIsImZ1bGxfbmFtZSI6IkpvaG4gRG9lIiwiZGlzYWJsZWQiOmZhbHNlLCJhZG1p"
    "biI6ZmFsc2UsImhhc2hlZF9wYXNzd29yZCI6IiQyYiQxMiRFaXhaYVlWSzFmc2J3MVpmYlgzT1hlUGFXeG4"
    "5NnAzNldRb2VHNkxydWozdmpQR2dhMzFsVyJ9.85AGZbGCPqZIjgbKqmdjJOqhzbT5HeTCTfIP6wJ_5PE"
)

if __name__ == "__main__":
    # populate(session=create_session(fetch_token()))
    populate(session=create_session(TOKEN))
