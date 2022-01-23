from typing import Optional

from snacksbar.utils import APIModel


class UserID(APIModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: bool = False
    admin: bool = False
