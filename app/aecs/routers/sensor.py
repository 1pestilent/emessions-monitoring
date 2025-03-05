from fastapi import APIRouter, Depends, HTTPException,status

from app.aecs import schemas
from app.models.database import session_dependency

router = APIRouter(prefix="/sensor",tags=["Sensor"])

@router.get('/{id}')
async def get_sensor_by_id(
    session: session_dependency,
    id: int,
):
    pass

@router.post('/create')
async def create_sensor(
    session: session_dependency,
    data: schemas.AddSensorSchema,
):
    ...

@router.post('/delete/{id}')
async def create_sensor(
    session: session_dependency,
    id: int
    ):
    ...

@router.put('/change')
async def change_sensor(
    session: session_dependency,
    data: schemas.AddSensorSchema,
):
    ...

@router.post('/calibration')
async def calibration_sensor(
    session: session_dependency,
    data: schemas.CalibrationSensorSchema,
):
    ...

@router.post('/installation')
async def installation_sensor(
    session: session_dependency,
    data: schemas.InstallationSensorSchema,
):
    ...

