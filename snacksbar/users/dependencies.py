from fastapi import Depends
from fastapi.security import SecurityScopes

from snacksbar.security import TokenData, create_exception, get_token_obj

from .dtos import UserID


def get_current_user(
    security_scopes: SecurityScopes, token: TokenData = Depends(get_token_obj)
):
    user = UserID(**token.dict())
    if user is None:
        raise create_exception(security_scopes)
    return user
