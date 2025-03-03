from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.aecs import schemas
from app.models.database import setup_database, session_dependency
from app.models.substances import StatusModel
from app.core import dictionary
from app.auth import utils as autils

router = APIRouter(prefix="/aecs",tags=["AECS"])


@router.get('/setup_db')
async def setup_db():
    return await setup_database()

@router.get('/create_statuses')
async def create_statuses(
    session: session_dependency
    ):
    for sensor_status in dictionary.statuses:
        result = await session.execute(select(StatusModel).where(StatusModel.id == sensor_status['id']))
        existing_status = result.scalars().first()

        if not existing_status:
            sensor_status = StatusModel(**sensor_status)
            session.add(sensor_status)

        else:
            raise HTTPException(status_code=409,
                                detail=f'Status: {sensor_status['name']!r} is already existed!')
    await session.commit()
    return {"status_code": status.HTTP_200_OK, "message": "Statuses successfully created."}
    

@router.get('/statuses')
async def get_statuses(
    session: session_dependency
) -> schemas.StatusesSchema:
    query = select(StatusModel)
    result = await session.execute(query)
    statuses = result.scalars().all()
    if not statuses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Statuses do not exist!') 
    status_schemas = [schemas.StatusSchema.from_orm(sensor_status) for sensor_status in statuses]
    response = schemas.StatusesSchema(statuses=status_schemas)
    
    return response

@router.get('/status/{id}')
async def get_status_by_id(
    id: int,
    session: session_dependency,
) -> schemas.StatusSchema:
    query = select(StatusModel).where(StatusModel.id == id)
    result = await session.execute(query)
    sensor_status = result.scalars().first()

    if not sensor_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Status with id: {id!r} does not exist')
    
    response = schemas.StatusSchema.from_orm(sensor_status)
    return response