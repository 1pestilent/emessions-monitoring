from typing import Annotated, Union

from fastapi import APIRouter, Depends, Request, Response, status
from fastapi.responses import RedirectResponse

from app.auth import create_token, utils
from app.auth.middleware import get_user_from_cookies
from app.templates import template
from app.auth.schemas import TokenSchema, UserLoginForm
from app.models.database import session_dependency
from app.users.schemas import SafelyUserSchema

router = APIRouter(prefix="/auth",tags=["Auth"])

@router.post('/token')
async def login_for_token(
    session: session_dependency,
    user: Annotated[UserLoginForm, Depends()],
) -> TokenSchema:
    
    user = await utils.authenticate_user(session, user.username, user.password)
    
    access_token = create_token.access_token(user)
    refresh_token = create_token.refresh_token(user)

    response = RedirectResponse(url="/", status_code=303)
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True)
    return response

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

@router.get('/')
async def login(
    request: Request,
    user: Union[SafelyUserSchema, RedirectResponse] = Depends(get_user_from_cookies),
    ):

    if isinstance(user, SafelyUserSchema):
        return RedirectResponse('/')
    
    response = template.TemplateResponse(request=request, name="login.html", context={"title": "Авторизация пользователя"})
    return response

@router.get('/logout')
def logout():
    response = RedirectResponse('/auth')
    response.delete_cookie('access_token')
    response.delete_cookie('refresh_token')
    return response