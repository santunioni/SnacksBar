from datetime import datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from jose import jwt

from snacksbar.constants import (
    ACCESS_TOKEN_EXPIRE_MINUTES,
    HASH_ALGORITHM,
    SIGNATURE_KEY,
)

from .dtos import Token
from .utils import get_authenticated_user

router = APIRouter(tags=["auth"])


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = get_authenticated_user(form_data.username, form_data.password)
    if user is None:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    data = {
        "sub": user.username,
        "scopes": form_data.scopes,
        "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
        **user.dict(exclude={"username"}),
    }
    access_token = jwt.encode(data, SIGNATURE_KEY, algorithm=HASH_ALGORITHM)
    return {"access_token": access_token, "token_type": "bearer"}
