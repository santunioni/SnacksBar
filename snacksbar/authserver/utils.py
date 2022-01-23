from typing import Optional

from passlib.context import CryptContext

from .dtos import UserID, UserInDB

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Chains",
        "email": "alicechains@example.com",
        "hashed_password": "$2b$12$gSvqqUPvlXP2tfVFaWK1Be7DlH.PKZbv5H8KnzzVgXXbVxpva.pFm",
        "disabled": True,
    },
}


def get_user_in_db(username: str) -> Optional[UserInDB]:
    """Function from the authentification server to fetch the user data."""
    if username in fake_users_db:
        user_dict = fake_users_db[username]
        return UserInDB(**user_dict)


def get_authenticated_user(username: str, password: str) -> Optional[UserID]:
    user = get_user_in_db(username)
    if user is None or not pwd_context.verify(password, user.hashed_password):
        return None
    return user
