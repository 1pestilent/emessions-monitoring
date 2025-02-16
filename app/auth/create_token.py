from datetime import timedelta

from app.core.security import encode_jwt
from app.users.schemas import UserSchema
from app.core.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE, REFRESH_TOKEN_EXPIRE_DAYS

async def access_token(user: UserSchema,
                            expire_timedelta: int | None = None
                            ) -> str:
    payload = {
        "sub": user.username,
        "fullname": user.last_name + user.first_name,
        }
    return encode_jwt(
         token_type=ACCESS_TOKEN_TYPE,
         payload=payload,
         expire_timedelta= expire_timedelta
    )

async def refresh_token(user: UserSchema,
    expire_timedelta: int | None = None
    ) -> str:
    payload = {
        "sub": user.username,
        }
    return encode_jwt(
         token_type=REFRESH_TOKEN_TYPE,
         payload=payload,
         expire_timedelta= timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
    )