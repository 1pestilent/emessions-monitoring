from typing import Annotated, Union

from fastapi import APIRouter, Request, Depends, Response
from fastapi.responses import RedirectResponse

from app.templates import template
from app.auth.middleware import is_authorized

router = APIRouter()

@router.get('/')
async def workspace(
    request: Request,
    authorization: Union[Response, str, True] = Depends(is_authorized),
    ):
    response = template.TemplateResponse(request=request, name="dashboard.html", context={"title": "Дашборд"})

    if isinstance(authorization, RedirectResponse):
        return authorization
    elif isinstance(authorization, str):
        response.set_cookie(key="access_token", value=authorization)

    return response