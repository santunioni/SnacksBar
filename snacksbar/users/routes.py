from fastapi import APIRouter, Depends
from starlette.exceptions import HTTPException

from snacksbar.security import Scopes

from .dependencies import get_current_user
from .dtos import UserID

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserID, dependencies=[Scopes.READ_USERS_ME.fastapi])
async def read_users_me(
    current_user: UserID = Depends(get_current_user),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
