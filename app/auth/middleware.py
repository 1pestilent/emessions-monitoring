from typing import Union, Annotated

from fastapi import Request, Depends, Cookie, HTTPException, status
from fastapi.responses import RedirectResponse

from app.auth.utils import get_new_access_token, validate_token, get_current_user_from_token
from app.core.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE 
from app.models.database import session_dependency
from app.users.schemas import SafelyUserSchema

redirect_to_auth = RedirectResponse('/auth')
redirect_to_auth.delete_cookie('access_token')
redirect_to_auth.delete_cookie('refresh_token')

async def is_authorized(
        session: session_dependency,
        access_token: Union[str, None] = Cookie(None),
        refresh_token: Union[str, None] = Cookie(None),
    )-> Union[str, RedirectResponse]:

    if validate_token(access_token):
        return access_token
    else:
        if validate_token(refresh_token, REFRESH_TOKEN_TYPE):
            new_token = await get_new_access_token(session, refresh_token)
            return new_token
        

async def get_user_from_cookies(
        session: session_dependency,
        token: Union[str, RedirectResponse] = Depends(is_authorized)
) -> SafelyUserSchema | RedirectResponse:
    
    if isinstance(token, RedirectResponse):
        return token
    try:
        user = await get_current_user_from_token(token, session)
    except HTTPException as e:
        if e.status_code == 401 or 403 or 404:
            return redirect_to_auth
        raise 
    return user