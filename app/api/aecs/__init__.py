from fastapi import APIRouter

from app.api.aecs.sensors import views as sensors
from app.api.aecs.status import views as status_router
from app.api.aecs.substances import views as substances
from app.api.aecs.units import views as units

router = APIRouter(prefix="/aecs")

router.include_router(units.router)
router.include_router(status_router.router)
router.include_router(substances.router)
router.include_router(sensors.router)