from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.aecs.units import schemas, utils
from app.models.aecs import UnitModel
from app.models.database import session_dependency

router = APIRouter(prefix="/unit",tags=["Unit"])

@router.get('/all')
async def get_units(
    session: session_dependency
) -> schemas.UnitListSchema:
    result = await session.execute(select(UnitModel))
    units = result.scalars().all()

    if not units:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Units do not exist!') 

    response = schemas.UnitListSchema(units=[schemas.UnitSchema.from_orm(unit) for unit in units])
    return response

@router.get('/{id}')
async def get_unit_by_id(
    id: int,
    session: session_dependency,
    ) -> schemas.UnitSchema:
    
    return schemas.UnitSchema.from_orm(await utils.get_unit_by_id(session, id))