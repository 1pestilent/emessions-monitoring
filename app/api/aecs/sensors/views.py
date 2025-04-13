from datetime import datetime
from typing import Annotated, Optional

from fastapi import APIRouter, Query, Form, HTTPException, status
from sqlalchemy import asc, select
from sqlalchemy.exc import IntegrityError

from app.api.aecs.sensors import utils
from app.api.aecs.sensors.schemas import (AddSensorReadingsSchema, AddSensorSchema,
                                      ChangeSensorSchema, ReadingListSchema,
                                      ReadingsSchema,
                                      ResponseAverageReadingSchema,
                                      SensorViewSchema, LocationSchema)
from app.api.aecs.status.utils import get_status_by_id
from app.api.aecs.units.utils import get_unit_by_id
from app.models.aecs import SensorModel, LocationModel
from app.models.database import session_dependency

router = APIRouter(prefix="/sensors",tags=["Sensor"])

@router.post('/create')
async def create_sensor(
    session: session_dependency,
    data: Annotated[AddSensorSchema, Form()],
) -> SensorViewSchema:
    
    result = await session.execute(
        select(SensorModel)
        .where(SensorModel.serial_number == data.serial_number)
        )
    sensor = result.first()

    if sensor:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Sensor with {data.serial_number!r} serial number already exists')
    
    try: 
        sensor = SensorModel(
            name=data.name,
            serial_number=data.serial_number,
            unit_id=data.unit_id,
            description=data.description,
            status=data.status
        )

        session.add(sensor)
        await session.commit()
        await session.refresh(sensor)

        return await utils.get_sensor_by_id(session, sensor.id)
    
    except IntegrityError as e:

        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error: {e!r}')

@router.get('/all')
async def get_sensors(
    session: session_dependency
):
    return await utils.get_sensors(session)

@router.get('/{id}')
async def get_sensor_by_id(
    session: session_dependency,
    id: int,
) -> SensorViewSchema:

    return await utils.get_sensor_by_id(session, id)

@router.delete('/delete/{id}')
async def delete_sensor_by_id(
    session: session_dependency,
    id: int,
    ):

    sensor = await utils.get_sensor_obj_by_id(session, id)
    await session.delete(sensor)
    await session.commit()

    return {"message": f"The sensor with ID {id} has been successfully deleted"}

@router.put('/change')
async def change_sensor(
    session: session_dependency,
    data: Annotated[ChangeSensorSchema, Form()],
    sensor_id: int,
) -> SensorViewSchema:
    
    sensor = await utils.get_sensor_obj_by_id(session, sensor_id)

    if data.name:
        sensor.name = data.name
    if data.serial_number:
        sensor.serial_number = data.serial_number
    if data.unit_id:
        try:
            if await get_unit_by_id(session, data.unit_id):
                sensor.unit_id = data.unit_id
        except HTTPException as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail=f'The sensor was not updated. Error: {e.detail.lower()}')
    if data.description:
        sensor.description = data.description
    if data.status:
        try:
            if await get_status_by_id(session, data.status):
                sensor.status = data.status
        except HTTPException as e:
            raise HTTPException(status.HTTP_400_BAD_REQUEST,detail=f'The sensor was not updated. Error: {e.detail.lower()}')
        
    await session.commit()
    await session.refresh(sensor)
    
    response = await utils.get_sensor_by_id(session, sensor_id)
    return response

@router.post('/installation')
async def installation_sensor(
    session: session_dependency,
    sensor_id: int,
    date: datetime,
) -> SensorViewSchema:  
    
    sensor = await utils.get_sensor_obj_by_id(session, sensor_id)

    sensor.installation_date = date
    await session.commit()
    await session.refresh(sensor)
    
    response = await utils.get_sensor_by_id(session, sensor_id)
    return response

@router.post('/calibration')
async def calibration_sensor(
    session: session_dependency,
    sensor_id: int,
    date: datetime,
) -> SensorViewSchema:  
    
    sensor = await utils.get_sensor_obj_by_id(session, sensor_id)

    sensor.calibration_date = date
    await session.commit()
    await session.refresh(sensor)
    
    response = await utils.get_sensor_by_id(session, sensor_id)
    return response

@router.post('/readings/record')
async def record_readings(
    session: session_dependency,
    data: Annotated[AddSensorReadingsSchema, Form()],
):
    try:
        if await get_sensor_by_id(session, data.sensor_id):
            return await utils.record_sensor_readings(session, data.sensor_id, data.value)
    except HTTPException as error:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, detail=f'Failed to record data. Error: {error.detail.lower()}')
    
@router.get('/readings/get/')
async def get_readings(
    session: session_dependency,
    sensor_id: int,
    day: int = Query(default=0, description='День, за который нужно вывести показания. По умолчанию - текущий.', ge=0,le=31),
    month: int = Query(default=0, description='Месяц, за который нужно вывести показания. По умолчанию - текущий.', ge=0,le=12),
    startdate: datetime | None = None,
    enddate: datetime | None = None,
) -> ReadingListSchema:
    readings = await utils.get_readings(
        session=session,
        sensor_id=sensor_id,
        day=day,
        month=month,
        startdate = startdate,
        enddate = enddate,
    )

    return ReadingListSchema(readings=[ReadingsSchema.from_orm(reading) for reading in readings])

@router.get('/readings/get/stats')
async def get_readings_stats(
    session: session_dependency,
    sensor_id: int,
    day: int = Query(default=0, description='День, за который нужно вывести показания. По умолчанию - текущий.', ge=0,le=31),
    month: int = Query(default=0, description='Месяц, за который нужно вывести показания. По умолчанию - текущий.', ge=0,le=12),
    startdate: datetime | None = None,
    enddate: datetime | None = None,
):
    return await utils.get_readings_stats(session, sensor_id, day, month, startdate, enddate)

@router.post('/location/create')
async def create_location(
    session: session_dependency,
    data: Annotated[LocationSchema, Form()],   
):  
    result = await session.execute(
        select(LocationModel)
        .where(LocationModel.name == data.name)
        )
    location = result.first()

    if location:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Location {data.name!r} already exists')
      
    try: 
        location = LocationModel(
            name=data.name,
            description=data.description,
        )

        session.add(location)
        await session.commit()
        await session.refresh(location)

        return {"message": "Location created successfully"}
    
    except IntegrityError as e:

        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error: {e!r}')

@router.get('/locations/all')
async def get_locations(
    session: session_dependency,
):
    locations = await utils.get_locations(session)
    return locations

@router.get('/link/{location_id}')
async def get_sensors_link(
    session: session_dependency,
    location_id: int,
):
    return await utils.get_sensors_link(session, location_id)

@router.post('/links/create/')
async def link(
    session: session_dependency,
    sensor_id: int,
    location_id: int,
):
    return await utils.link_sensor(session, sensor_id, location_id)

@router.get('/{sensor_id}/readings/last')
async def get_last_readings(
    session: session_dependency,
    sensor_id: int,
):
    return await utils.get_last_readings(session, sensor_id)