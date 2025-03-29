from typing import Union, Annotated

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.templates import template
from app.api.users.schemas import SafelyUserSchema
from app.api.auth.middleware import get_user_from_cookies
from app.models.database import session_dependency
from app.api.aecs.sensors.utils import get_locations

 
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