from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import RedirectResponse


from app.api.auth.utils import validate_token, get_new_access_token
from app.models.database import new_session
from app.core.config import PUBLIC_PATHS, PUBLIC_PATH_PREFIXES, AUTH_PATH

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(
            self,
            request: Request,
            call_next,
            ):
        
        response = await call_next(request)

        access_token = request.cookies.get('access_token')
        refresh_token = request.cookies.get('refresh_token')

        if request.url.path == AUTH_PATH:
            redirect = RedirectResponse('/')
            if validate_token(access_token):
                return redirect
            
            async with new_session() as session:
                new_access_token = await get_new_access_token(session, refresh_token)
            if new_access_token:
                redirect.set_cookie(key="access_token",value=new_access_token)
                return redirect
        
            return response

        if any(request.url.path.startswith(prefix) for prefix in PUBLIC_PATH_PREFIXES) or request.url.path in PUBLIC_PATHS:
            return response
        
        if validate_token(access_token):
            return response
        
        async with new_session() as session:
            new_access_token = await get_new_access_token(session, refresh_token)
        if new_access_token:
            response.set_cookie(key="access_token",value=new_access_token)
            return response

        return RedirectResponse('/login')