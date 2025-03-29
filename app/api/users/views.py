from typing import Annotated

from fastapi import APIRouter, Depends, Form

from app.api.auth import utils as autils
from app.models.database import session_dependency
from app.api.users import utils
from app.api.users.schemas import SafelyUserSchema, UserAddSchema, UserSchema

router = APIRouter(prefix="/users", tags=["User"])

@router.post('/add')
async def add_user(
    new_user: Annotated[UserAddSchema, Form()],
    session: session_dependency,
    ) -> int:
    if await utils.user_is_uniq(session, new_user.username, new_user.email):
        user_id = await utils.create_user(session, new_user)
        # переделать ответ
        return user_id 

@router.get('/get/{username}',
            dependencies=[Depends(autils.http_bearer)],
            )
async def get_user_by_username(
    username: str,
    session: session_dependency,
    user: Annotated[SafelyUserSchema, Depends(autils.get_current_user)],
) -> SafelyUserSchema:
    user: UserSchema = await utils.get_user(session, username)
    return utils.return_safe_user(user)