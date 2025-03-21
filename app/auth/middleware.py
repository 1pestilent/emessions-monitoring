from typing import Union, Annotated

from fastapi import Request, Response, Depends, Cookie
from fastapi.responses import RedirectResponse

from app.auth.utils import get_token_payload, get_new_access_token, validate_token_type
from app.core.config import ACCESS_TOKEN_TYPE
from app.models.database import session_dependency

auth_redirect = RedirectResponse('/auth')
auth_redirect.delete_cookie("access_token")
auth_redirect.delete_cookie("refresh_token")



async def is_authorized(
        session: session_dependency,
        access_token: Union[str, None] = Cookie(None),
        refresh_token: Union[str, None] = Cookie(None),
    )-> Union[Response, None]:
    
    auth_redirect = RedirectResponse('/auth')
    auth_redirect.delete_cookie("access_token")
    auth_redirect.delete_cookie("refresh_token")

    if not access_token and not refresh_token:
        return auth_redirect
    
    payload = get_token_payload(access_token)
    if payload is None or not validate_token_type(payload, ACCESS_TOKEN_TYPE):
        new_access_token = await get_new_access_token(session, refresh_token)
        return new_access_token if new_access_token else auth_redirect
            
    return True
