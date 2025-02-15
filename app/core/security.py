import bcrypt
import jwt
from datetime import datetime, timedelta

from app.core.config import PUBLIC_KEY_PATH, PRIVATE_KEY_PATH, TOKEN_TYPE_FIELD, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    pwd_bytes: bytes = password.encode()
    return bcrypt.hashpw(pwd_bytes, salt)


def verify_password(password: str, hashed_password: bytes) -> bool:
    return bcrypt.checkpw(password=password.encode(), hashed_password=hashed_password)


def encode_jwt(
        token_type: str,
        payload: dict,
        expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES,
        expire_timedelta: timedelta | None = None,
        ) -> str:

    now = datetime.utcnow()
    to_encode = payload.copy()


    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    to_encode.update(
        TOKEN_TYPE_FIELD = token_type,
        iat = now,
        exp = expire
        )

    encoded = jwt.encode(to_encode, PRIVATE_KEY_PATH.read_text(), ALGORITHM)
    return encoded


def decode_jwt(token: str | bytes) -> dict:

    decoded = jwt.decode(
        token,
        PUBLIC_KEY_PATH.read_text(),
        algorithms=[ALGORITHM]
        )
    return decoded