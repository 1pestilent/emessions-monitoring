from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.aecs.status import utils
from app.aecs.status.schemas import StatusListSchema, StatusSchema
from app.models.aecs import StatusModel
from app.models.database import session_dependency

router = APIRouter(prefix="/status",tags=["Status"])

@router.get('/all')
async def get_statuses(
    session: session_dependency
) -> StatusListSchema:
    result = await session.execute(select(StatusModel))
    statuses = result.scalars().all()

    if not statuses:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='No statuses exist!') 
    
    response = StatusListSchema(statuses=[StatusSchema.from_orm(sensor_status) for sensor_status in statuses])
    return response

@router.get('/{id}')
async def get_status_by_id(
    id: int,
    session: session_dependency,
) -> StatusSchema:
    sensor_status = await utils.get_status_by_id(session, id)

    response = StatusSchema.from_orm(sensor_status)
    return response