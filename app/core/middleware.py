from fastapi import Request, Cookie
from starlette.middleware.base import BaseHTTPMiddleware

from fastapi.responses import RedirectResponse
from app.api.auth.utils import validate_token, get_new_access_token
from app.models.database import session_dependency

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next,
            ):
        session = session_dependency
        if request.url.path.startswith("/static") or request.url.path.startswith("/api") or request.url.path in ["/login", "/docs", "/openapi.json"]:
            return await call_next(request)
        
        access_token: str = Cookie('access_token'),
        refresh_token: str = Cookie('refresh_token'),
        
        if validate_token(access_token): 
            return await call_next(request)
    
        new_access = await get_new_access_token(session, refresh_token)
        if new_access:
            return await call_next(request)
    
        return RedirectResponse('/login')