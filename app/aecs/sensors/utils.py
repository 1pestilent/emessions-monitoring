from fastapi import HTTPException, status
from sqlalchemy import select, asc
from sqlalchemy.ext.asyncio import AsyncSession 
import asyncio

from app.aecs.sensors.schemas import SensorViewSchema, SensorViewListSchema
from app.models.database import session_dependency, get_session
from app.models.substances import SensorModel, UnitModel, StatusModel

sensor_query = (
    select(
        SensorModel.id,
        SensorModel.name,
        SensorModel.serial_number,
        UnitModel.symbol, 
        SensorModel.installation_date, 
        SensorModel.calibration_date, 
        SensorModel.description,
        StatusModel.name,
        )
        .join(UnitModel)
        .join(StatusModel)
        .order_by(asc(SensorModel.id))
    )

def sensor_to_schema(sensor: dict) -> SensorViewSchema:
    response = SensorViewSchema(
        id=sensor.id,
        name=sensor.name,
        serial_number=sensor.serial_number,
        unit_symbol=sensor.symbol,
        installation_date=sensor.installation_date,
        calibration_date=sensor.calibration_date,
        description=sensor.description,
        status_name=sensor.name_1)
    return response

async def get_sensors(
        session: AsyncSession,
):
    result = await session.execute(sensor_query)
    sensors = result.all()

    if not sensors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Anyone sensors does not exist')

    response = SensorViewListSchema(sensors=[sensor_to_schema(sensor) for sensor in sensors])
    
    return response

async def get_sensor_by_id(
        session: AsyncSession,
        id: int,
) -> SensorViewSchema:

    result = await session.execute(sensor_query.where(SensorModel.id == id))
    sensor = result.first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Sensor with {id!r} id does not exist')
    
    return sensor_to_schema(sensor)

async def get_sensor_by_serial(
        session: AsyncSession,
        serial_number: str,
) -> SensorViewSchema:
    
    result = await session.execute(sensor_query.where(SensorModel.serial_number == serial_number))
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Sensor with {serial_number!r} serial number does not exist')
    
    return sensor_to_schema(sensor)

async def get_sensor_obj_by_id(
        session: AsyncSession,
        id: int,
    ) -> SensorModel:
    result = await session.execute(select(SensorModel).where(SensorModel.id == id))
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Sensor with {id!r} id does not exist')
    
    return sensor

async def get_sensor_obj_by_serial(
        session: AsyncSession,
        serial_number: int,
    ) -> SensorModel:
    result = await session.execute(select(SensorModel).where(SensorModel.serial_number == serial_number))
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'Sensor with {id!r} id does not exist')
    
    return sensor