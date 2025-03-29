from typing import Union, Annotated

from fastapi import Request, Depends, Cookie, HTTPException, status
from fastapi.responses import RedirectResponse

from app.api.auth.utils import get_new_access_token, validate_token, get_current_user_from_token
from app.core.config import ACCESS_TOKEN_TYPE, REFRESH_TOKEN_TYPE 
from app.models.database import session_dependency
from app.api.users.schemas import SafelyUserSchema

redirect_to_auth = RedirectResponse('/auth')
redirect_to_auth.delete_cookie('access_token')
redirect_to_auth.delete_cookie('refresh_token')

async def is_authorized(
        session: session_dependency,
        access_token: Union[str, None] = Cookie(None),
        refresh_token: Union[str, None] = Cookie(None),
    )-> Union[str, None]:

    if not access_token and not refresh_token:
        return None
    
    if validate_token(access_token):
        return access_token

    if validate_token(refresh_token, REFRESH_TOKEN_TYPE):
        new_token = await get_new_access_token(session, refresh_token)
        return new_token
    return None

async def get_user_from_cookies(
        request: Request,
        session: session_dependency,
        current_token: Union[str, None] = Cookie(None),
        new_token: Union[str, None] = Depends(is_authorized)
) -> SafelyUserSchema | RedirectResponse:
    
    if not new_token:
        return redirect_to_auth
    
    try:
        print(current_token != new_token)
        if current_token != new_token:
            response = RedirectResponse(str(request.url))
            response.set_cookie('access_token', new_token)
            return response
        
        user = await get_current_user_from_token(new_token, session)

    except HTTPException as e:
        if e.status_code == 401 or 403 or 404:
            return redirect_to_auth
        raise 
    return user