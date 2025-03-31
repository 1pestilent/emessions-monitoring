from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.auth import create_token, utils
from app.api.auth.schemas import TokenSchema, UserLoginForm
from app.models.database import session_dependency
from app.api.users.schemas import SafelyUserSchema

router = APIRouter(prefix="/login",tags=["Authorization"])

@router.post('/')
async def login_for_token(
    session: session_dependency,
    user: Annotated[UserLoginForm, Depends()],
) -> TokenSchema:
    
    user = await utils.authenticate_user(session, user.username, user.password)
    
    access_token = create_token.access_token(user)
    refresh_token = create_token.refresh_token(user)

    return TokenSchema(access_token=access_token, refresh_token=refresh_token)

@router.post("/refresh",
             response_model=TokenSchema,
             response_model_exclude_none=True,
             dependencies=[Depends(utils.http_bearer)],
             )
async def refresh_access_token(
    user: SafelyUserSchema = Depends(utils.get_current_user_for_refresh)
):
    access_token = await create_token.access_token(user)

    return TokenSchema(
        access_token=access_token
    )