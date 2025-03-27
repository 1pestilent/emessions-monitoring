from typing import Union

from fastapi import APIRouter, Request, Depends
from fastapi.responses import RedirectResponse

from app.templates import template
from app.users.schemas import SafelyUserSchema
from app.auth.middleware import get_user_from_cookies
from app.models.database import session_dependency

 
router = APIRouter()

@router.get('/')
async def workspace(
    request: Request,
    user: Union[SafelyUserSchema] = Depends(get_user_from_cookies),
    ):
    if isinstance(user, RedirectResponse):
        return user
    
    response = template.TemplateResponse(request=request, name="dashboard.html", context={"title": "Дашборд", "username": user.username})
    return response