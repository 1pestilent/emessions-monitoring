from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import select, asc
from sqlalchemy.exc import IntegrityError
from typing import Annotated, Optional
from datetime import datetime

from app.aecs.sensors import utils
from app.models.aecs import SensorModel
from app.aecs.sensors.schemas import AddSensorSchema, SensorViewSchema, ChangeSensorSchema
from app.aecs.units.utils import get_unit_by_id
from app.aecs.status.utils import get_status_by_id
from app.models.database import session_dependency

router = APIRouter(prefix="/sensor",tags=["Sensor"])

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

        return {"message": "Sensor created successfully", "sensor" : await utils.get_sensor_by_id(session, sensor.id)}
    
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