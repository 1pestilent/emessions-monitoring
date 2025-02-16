from fastapi import APIRouter, Form
from typing import Annotated

from app.models.database import session_dependency
from app.users.schemas import SafelyUserSchema, UserAddSchema, UserSchema
from app.users import utils

router = APIRouter(prefix="/users", tags=["User"])


@router.post('/add')
async def add_user(
    new_user: Annotated[UserAddSchema, Form()],
    session: session_dependency,
    ) -> int:
    if await utils.user_is_uniq(session, new_user.username, new_user.email):
        user_id = await utils.create_user(session, new_user)
        return user_id 

@router.get('/get/{username}')
async def get_user_by_username(
    username: str,
    session: session_dependency,
) -> SafelyUserSchema:
    user: UserSchema = await utils.get_user(session, username)
    return utils.return_safe_user(user)