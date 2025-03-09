from fastapi import APIRouter, Depends, Form, HTTPException, status
from sqlalchemy import select, asc
from sqlalchemy.exc import IntegrityError
from typing import Annotated

from app.models.substances import SensorModel, UnitModel, StatusModel
from app.aecs import schemas
from app.models.database import session_dependency

router = APIRouter(prefix="/sensor",tags=["Sensor"])

@router.post('/create')
async def create_sensor(
    session: session_dependency,
    data: Annotated[schemas.AddSensorSchema, Form()],

):
    query = select(SensorModel).where(SensorModel.serial_number == data.serial_number)
    result = await session.execute(query)
    result = result.all()

    if result:
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

        return {"message": "Sensor created successfully", "sensor_id": sensor.id}
    
    except IntegrityError as e:

        await session.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Error: {e!r}')

@router.get('/all')
async def get_sensors(
    session: session_dependency
) -> schemas.SensorListSchema:
    query = (select(SensorModel.id,
    SensorModel.name,
    SensorModel.serial_number,
    UnitModel.symbol, 
    SensorModel.installation_date, 
    SensorModel.calibration_date, 
    SensorModel.description,
    StatusModel.name
    )
    .join(UnitModel)
    .join(StatusModel)
    .order_by(asc(SensorModel.id))
    )

    results = await session.execute(query)
    sensors = results.all()

    if not sensors:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Anyone sensors does not exist')
    
    sensor_list = []
    for sensor_data in sensors:
        sensor = schemas.SensorSchema(
            id=sensor_data.id,
            name=sensor_data.name,
            serial_number=sensor_data.serial_number,
            unit_symbol=sensor_data.symbol,
            installation_date=sensor_data.installation_date,
            calibration_date=sensor_data.calibration_date,
            description=sensor_data.description,
            status_name=sensor_data.name_1
            )
        sensor_list.append(sensor)

    response = schemas.SensorListSchema(sensors = sensor_list)
    return response

@router.get('/{id}')
async def get_sensor_by_id(
    session: session_dependency,
    id: int,
) -> schemas.SensorSchema:
    query = (select(SensorModel.id,
                SensorModel.name,
                SensorModel.serial_number,
                UnitModel.symbol, 
                SensorModel.installation_date, 
                SensorModel.calibration_date, 
                SensorModel.description,
                StatusModel.name
                )
                .where(SensorModel.id == id)
                .join(UnitModel)
                .join(StatusModel)
                )
    result = await session.execute(query)
    sensor_data = result.first()
    if not sensor_data:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Sensor with {id} not found')
    sensor = schemas.SensorSchema(
        id=sensor_data.id,
        name=sensor_data.name,
        serial_number=sensor_data.serial_number,
        unit_symbol=sensor_data.symbol,
        installation_date=sensor_data.installation_date,
        calibration_date=sensor_data.calibration_date,
        description=sensor_data.description,
        status_name=sensor_data.name_1
        )
    
    return sensor

@router.delete('/delete/{id}')
async def delete_sensor_by_id(
    session: session_dependency,
    id: int
    ):

    query = select(SensorModel).where(SensorModel.id == id)
    result = await session.execute(query)
    sensor = result.scalar_one_or_none()

    if sensor is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Sensor with id {id} not found"
        )

    await session.delete(sensor)
    await session.commit()

    return {"message": f"Sensor with id {id} deleted successfully"}

@router.put('/change')
async def change_sensor(
    session: session_dependency,
    data: Annotated[schemas.ChangeSensorSchema, Form()],
    sensor_id: int,
):
    query = select(SensorModel).where(SensorModel.id == sensor_id)
    result = await session.execute(query)
    sensor = result.scalars().first()

    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor does not exist")
    
    if data.name:
        sensor.name = data.name
    if data.serial_number:
        sensor.serial_number = data.serial_number
    if data.unit_id:
        sensor.unit_id = data.unit_id
    if data.description:
        sensor.description = data.description
    if data.status:
        sensor.status = data.status
    
    await session.commit()
    await session.refresh(sensor)
    
    return sensor


@router.post('/installation')
async def installation_sensor(
    session: session_dependency,
    data: Annotated[schemas.InstallationSensorSchema, Form()],
    sensor_id: int,
):  
    if data.id:
        query = select(SensorModel).where(SensorModel.id == sensor_id)
        result = await session.execute(query)
        sensor = result.scalars().first()

        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor does not exist")
    else:
        query = select(SensorModel).where(SensorModel.serial_number == data.serial_number)
        result = await session.execute(query)
        sensor = result.scalars().first()

        if not sensor:
            raise HTTPException(status_code=404, detail="Sensor does not exist")
    ...
    
@router.post('/calibration')
async def calibration_sensor(
    session: session_dependency,
    data: Annotated[schemas.CalibrationSensorSchema, Form()],
):
    ...