from fastapi import APIRouter, Depends, Security
from fastapi.security import SecurityScopes
from starlette.exceptions import HTTPException

from snacksbar.security import TokenData, _create_exception, _get_token_obj

from .dtos import UserID

router = APIRouter(tags=["users"])


def get_current_user(
    security_scopes: SecurityScopes, token: TokenData = Depends(_get_token_obj)
):
    user = UserID(**token.dict())
    if user is None:
        raise _create_exception(security_scopes)
    return user


@router.get("/me", response_model=UserID)
async def read_users_me(
    current_user: UserID = Security(get_current_user, scopes=["me"]),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
