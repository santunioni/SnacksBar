from fastapi import APIRouter, Security
from starlette.exceptions import HTTPException

from .dependencies import get_current_user
from .dtos import UserID

router = APIRouter(tags=["users"])


@router.get("/me", response_model=UserID)
async def read_users_me(
    current_user: UserID = Security(get_current_user, scopes=["me"]),
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
