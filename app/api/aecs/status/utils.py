from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.aecs import StatusModel


async def get_status_by_id(
        session: AsyncSession,
        id: int
) -> StatusModel:
    
    result = await session.execute(select(StatusModel).where(StatusModel.id == id))
    sensor_status = result.scalars().first()

    if not sensor_status:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'The unit with ID {id} does not exist!')
    
    return sensor_status