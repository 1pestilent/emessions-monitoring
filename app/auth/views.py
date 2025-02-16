from fastapi import APIRouter, Form, Depends
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated

from app.auth import utils
from app.auth.schemas import TokenSchema, UserLoginForm
from app.auth import create_token
from app.models.database import session_dependency
from app.users.schemas import SafelyUserSchema

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post('/token')
async def login_for_token(
    session: session_dependency,
    user: Annotated[UserLoginForm, Depends()],
) -> TokenSchema:
    
    user = await utils.authenticate_user(session, user.username, user.password)
    
    access_token = await create_token.access_token(user)
    refresh_token = await create_token.refresh_token(user)

    return TokenSchema(
        access_token=access_token,
        refresh_token=refresh_token
    )
