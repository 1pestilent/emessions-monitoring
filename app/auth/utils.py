from fastapi import HTTPException, status

from app.models.database import session_dependency
from app.users.schemas import UserSchema, SafelyUserSchema
from app.users.utils import get_user, return_safe_user
from app.core import security


async def authenticate_user(
        session: session_dependency,
        username: str,
        password: str,
        ) -> SafelyUserSchema:
    user: UserSchema = await get_user(session, username)
    if not security.verify_password(password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect login or password",
            headers={"WWW-Authenticate": "Bearer"},
            )

    return return_safe_user(user)

