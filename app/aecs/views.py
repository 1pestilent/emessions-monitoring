from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.models.database import session_dependency
from app.auth import utils as autils

from app.aecs.routers import unit, status, substances, sensor

router = APIRouter(prefix="/aecs",tags=["AECS"])

router.include_router(unit.router)
router.include_router(status.router)
router.include_router(substances.router)
router.include_router(sensor.router)