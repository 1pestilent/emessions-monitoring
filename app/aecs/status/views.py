from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.aecs.status import schemas
from app.models.database import session_dependency
from app.models.substances import StatusModel

router = APIRouter(prefix="/status",tags=["Status"])

@router.get('/all')
async def get_statuses(
    session: session_dependency
) -> schemas.StatusListSchema:
    query = select(StatusModel)
    result = await session.execute(query)
    statuses = result.scalars().all()
    if not statuses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Statuses do not exist!') 
    statuses_schemas = [schemas.StatusSchema.from_orm(sensor_status) for sensor_status in statuses]
    response = schemas.StatusListSchema(statuses=statuses_schemas)
    
    return response

@router.get('/{id}')
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