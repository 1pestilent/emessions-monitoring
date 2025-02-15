from fastapi import APIRouter

from app.models.database import session_dependency
from app.users.schemas import UserAddSchema, UserSchema
from app.users import utils

router = APIRouter(prefix="/users", tags=["User"])


@router.post('/add')
async def add_user(
    new_user: UserAddSchema,
    session: session_dependency,
    ) -> int:
    user_id = await utils.create_user(session, new_user)
    return user_id

@router.get('/get/{username}')
async def get_user_by_username(
    username: str,
    session: session_dependency,
) -> UserSchema:
    user: UserSchema = await utils.get_user(session, username)
    return user
    