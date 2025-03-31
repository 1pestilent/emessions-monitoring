from fastapi import APIRouter

from app.api import aecs as aecs
from app.api.auth import views as auth
from app.api.users import views as users

router = APIRouter(prefix='/api', tags=["API"])

router.include_router(users.router)
router.include_router(auth.router)
router.include_router(aecs.router)