from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.aecs.units import schemas
from app.models.substances import UnitModel
from app.models.database import session_dependency

router = APIRouter(prefix="/unit",tags=["Unit"])

@router.get('/all')
async def get_units(
    session: session_dependency
) -> schemas.UnitListSchema:
    query = select(UnitModel)
    result = await session.execute(query)
    units = result.scalars().all()

    if not units:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Units do not exist!') 
    
    units_schemas = [schemas.UnitSchema.from_orm(unit) for unit in units]
    response = schemas.UnitListSchema(units=units_schemas)
    return response

@router.get('/{id}')
async def get_unit_by_id(
    id: int,
    session: session_dependency,
) -> schemas.UnitSchema:
    query = select(UnitModel).where(UnitModel.id == id)
    result = await session.execute(query)
    unit = result.scalars().first()

    if not unit:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'Unit with id: {id!r} does not exist')
    
    response = schemas.UnitSchema.from_orm(unit)
    return response