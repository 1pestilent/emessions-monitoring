from fastapi import APIRouter, Depends, status
from sqlalchemy import select

from app.aecs.sensors import views as sensors
from app.aecs.status import views as status
from app.aecs.substances import views as substances
from app.aecs.units import views as units

router = APIRouter(prefix="/aecs",tags=["AECS"])

router.include_router(units.router)
router.include_router(status.router)
router.include_router(substances.router)
router.include_router(sensors.router)