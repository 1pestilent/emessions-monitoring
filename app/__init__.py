from fastapi import APIRouter

from app.aecs import views as aecs
from app.aecs.routers import create
from app.auth import views as auth
from app.users import views as users

router = APIRouter()

router.include_router(users.router)
router.include_router(auth.router)
router.include_router(aecs.router)
router.include_router(create.router)