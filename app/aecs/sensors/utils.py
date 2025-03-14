from fastapi import HTTPException, status
from sqlalchemy import select, asc, func
from sqlalchemy.ext.asyncio import AsyncSession 
from datetime import datetime

from app.aecs.sensors.schemas import SensorViewSchema, SensorViewListSchema
from app.models.database import session_dependency, get_session
from app.models.aecs import SensorModel, UnitModel, StatusModel, SensorReadingsModel

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
        startdate: datetime | None,
        enddate: datetime | None,
        average: bool = False,
):
    if not average:
        query = select(SensorReadingsModel).where(SensorReadingsModel.sensor_id == sensor_id)
    else: 
        query = select(func.avg(SensorReadingsModel.value)).where(SensorReadingsModel.sensor_id == sensor_id)
        
    if startdate and enddate:
        query = query.where(SensorReadingsModel.timestamp >= startdate, SensorReadingsModel.timestamp <= enddate)
    elif startdate:
        query = query.where(SensorReadingsModel.timestamp >= startdate)
    elif enddate:
        query = query.where(SensorReadingsModel.timestamp <= enddate)

    result = await session.execute(query)
    readings = result.scalars().all()

    if not readings:
        raise HTTPException(status_code=404, detail="No readings found for the given criteria")

    return readings