import itertools
from enum import Enum
from typing import List, Optional

from astroid.decorators import cachedproperty
from fastapi import Depends, HTTPException, Security, status
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


_oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="auth/token",
    scopes={
        "me": "Information about the user",
        "products:read": "Read information about all products.",
        "products:modify": "Create/update/delete all products.",
    },
)


def get_token_obj(token: str = Depends(_oauth2_scheme)) -> Optional[TokenData]:
    try:
        return TokenData.parse_obj(
            jwt.decode(token, SIGNATURE_KEY, algorithms=[HASH_ALGORITHM])
        )
    except (JWTError, ValidationError):
        return None


def _create_exception(
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


def _check_credentials(
    security_scopes: SecurityScopes,
    token_obj: Optional[TokenData] = Depends(get_token_obj),
) -> None:
    if token_obj is None:
        raise _create_exception(security_scopes)
    required_not_granted = tuple(
        itertools.filterfalse(token_obj.scopes.__contains__, security_scopes.scopes)
    )
    if len(required_not_granted) > 0:
        raise _create_exception(
            security_scopes,
            detail=f"Not enough permissions. Missing scopes='{' '.join(required_not_granted)}'",
        )


class Scopes(Enum):
    CHANGE_PRODUCTS = "products:modify"
    READ_PRODUCTS = "products:read"
    READ_USERS_ME = "me"

    @cachedproperty
    def fastapi(self) -> Security:
        return Security(
            _check_credentials, scopes=self.value.split(" "), use_cache=False
        )

    def __str__(self):
        return self.value
