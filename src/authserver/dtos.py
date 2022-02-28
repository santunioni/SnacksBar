from typing import Optional

from snacksbar.utils import APIModel


class Token(APIModel):
    access_token: str
    token_type: str


class UserID(APIModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
    admin: bool = False


class UserInDB(UserID):
    hashed_password: str
