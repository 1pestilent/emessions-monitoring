from fastapi import APIRouter, Request, Cookie
from fastapi.responses import RedirectResponse

from app.api.auth.utils import validate_token, get_new_access_token
from app.templates import template
from app.core.config import REFRESH_TOKEN_TYPE
from app.models.database import session_dependency

router = APIRouter(tags=['Dashboard'])

@router.get('/')
async def workspace(
    request: Request,
    ):
    response = template.TemplateResponse(request=request, name="dashboard.html", context={"title": "Дашборд"})
    return response

@router.get('/login')
async def login(
    request: Request,
):
    response = template.TemplateResponse(request=request, name="login.html", context={"title": "Авторизация пользователя"})
    return response