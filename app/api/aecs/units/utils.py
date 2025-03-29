from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.aecs.units.schemas import UnitSchema
from app.models.aecs import UnitModel


async def get_unit_by_id(
        session: AsyncSession,
        id: int,
) -> UnitModel:
    
    result = await session.execute(select(UnitModel).where(UnitModel.id == id))
    unit = result.scalars().first()

    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'The unit with ID {id} does not exist!')
    return unit
