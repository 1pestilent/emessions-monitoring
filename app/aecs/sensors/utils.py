from datetime import datetime, timedelta

from fastapi import HTTPException, status, Query
from sqlalchemy import asc, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.aecs.sensors.schemas import SensorViewListSchema, SensorViewSchema
from app.models.aecs import (SensorModel, SensorReadingsModel, StatusModel,
                             UnitModel)
from app.models.database import get_session, session_dependency

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
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'No sensors exist')

    response = SensorViewListSchema(sensors=[sensor_to_schema(sensor) for sensor in sensors])
    
    return response

async def get_sensor_by_id(
        session: AsyncSession,
        id: int,
) -> SensorViewSchema:

    result = await session.execute(sensor_query.where(SensorModel.id == id))
    sensor = result.first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'The sensor with ID {id} does not exist')
    
    return sensor_to_schema(sensor)

async def get_sensor_by_serial(
        session: AsyncSession,
        serial_number: str,
) -> SensorViewSchema:
    
    result = await session.execute(sensor_query.where(SensorModel.serial_number == serial_number))
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'The sensor with serial number {serial_number!r} does not exist')
    
    return sensor_to_schema(sensor)

async def get_sensor_obj_by_id(
        session: AsyncSession,
        id: int,
    ) -> SensorModel:
    result = await session.execute(select(SensorModel).where(SensorModel.id == id))
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'The sensor with ID {id} does not exist')
    
    return sensor

async def get_sensor_obj_by_serial(
        session: AsyncSession,
        serial_number: int,
    ) -> SensorModel:
    result = await session.execute(select(SensorModel).where(SensorModel.serial_number == serial_number))
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail=f'The sensor with serial number {serial_number!r} does not exist')
    
    return sensor

async def record_sensor_readings(
        session: AsyncSession,
        sensor_id: int,
        value: float,
):
    try:
        readings = SensorReadingsModel(
            sensor_id = sensor_id,
            value = value,
            timestamp = datetime.now())
        
        session.add(readings)
        await session.commit()
        await session.refresh(readings)
        return {"detail": f"Data recorded successfully", "id": readings.id}
    except Exception as error:
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Failed to record sensor reading. Error: {error}")

async def get_readings(
        session: session_dependency,
        sensor_id: int,
        day: int = 0,
        month: int = 0,
        startdate: datetime | None = None,
        enddate: datetime | None = None,
):
    query = select(SensorReadingsModel).where(SensorReadingsModel.sensor_id == sensor_id)

    if (startdate or enddate) and not (day or month):
        if startdate:
            query = query.where(SensorReadingsModel.timestamp >= startdate)
        if enddate:
            query = query.where(SensorReadingsModel.timestamp <= enddate)
    elif not (startdate or enddate) and (day or month):
        now = datetime.now()
        if day and not month:
            query = query.where(SensorReadingsModel.timestamp >= datetime(now.year, now.month, now.day))
        if not day and month:
            query = query.where(SensorReadingsModel.timestamp >= datetime(now.year, now.month, 1))
        if day and month:
            raise HTTPException(status.HTTP_400_BAD_REQUEST)

    result = await session.execute(query)
    readings = result.scalars().all()

    if not readings:
        raise HTTPException(status_code=404, detail="No readings found for the given criteria")
    return readings