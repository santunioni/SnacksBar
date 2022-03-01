from snacksbar.users.dtos import UserID
from snacksbar.utils import APIModel


class Token(APIModel):
    access_token: str
    token_type: str


class UserInDB(UserID):
    hashed_password: str
