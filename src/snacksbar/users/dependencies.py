from typing import Optional

from fastapi import Depends

from snacksbar.security import TokenData, get_token_obj

from .dtos import UserID


def get_current_user(
    token: Optional[TokenData] = Depends(get_token_obj),
) -> Optional[UserID]:
    if token is None:
        return None
    user = UserID(**token.dict())
    return user
