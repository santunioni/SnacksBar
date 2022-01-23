import itertools
from typing import List, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jose import JWTError, jwt
from pydantic import Field, ValidationError

from snacksbar.constants import HASH_ALGORITHM, SIGNATURE_KEY
from snacksbar.users.dtos import UserID


class TokenData(UserID):
    username: Optional[str] = Field(..., alias="sub")
    scopes: List[str] = Field(default_factory=list)

    @property
    def sub(self) -> str:
        return self.username


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "me": "Information about the user",
        "products:read": "Read information about all products.",
        "products:modify": "Create/update/delete all products.",
    },
)


def create_exception(
    security_scopes: SecurityScopes, detail: Optional[str] = None
) -> HTTPException:
    authenticate_value = "Bearer"
    if security_scopes.scopes:
        authenticate_value += f' scope="{security_scopes.scope_str}"'
    return HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=detail or "Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )


def get_token_obj(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme)
) -> TokenData:
    try:
        return TokenData.parse_obj(
            jwt.decode(token, SIGNATURE_KEY, algorithms=[HASH_ALGORITHM])
        )
    except (JWTError, ValidationError) as err:
        raise create_exception(security_scopes) from err


def check_credentials(
    security_scopes: SecurityScopes, token: TokenData = Depends(get_token_obj)
) -> None:
    required_not_granted = tuple(
        itertools.filterfalse(token.scopes.__contains__, security_scopes.scopes)
    )
    if len(required_not_granted) > 0:
        raise create_exception(
            security_scopes,
            detail=f"Not enough permissions. Missing scopes='{' '.join(required_not_granted)}'",
        )
