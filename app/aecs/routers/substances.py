from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.aecs import schemas
from app.models.database import session_dependency
from app.models.substances import SubstanceModel, StatusModel, UnitModel

router = APIRouter(prefix="/substance",tags=["Substance"])

@router.get('/all')
async def get_substances(
    session: session_dependency
):
    query = select(SubstanceModel.id, SubstanceModel.name, UnitModel.symbol, SubstanceModel.mpc).join(UnitModel)
    result = await session.execute(query)
    substances = result.all()
    if not substances:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Substances do not exist!')
    substances_schema = [schemas.SubstanceSchema(
            id=substance[0],
            name=substance[1],
            unit_symbol=substance[2],
            mpc=substance[3]
        )
        for substance in substances]
    response = schemas.SubstanceListSchema(substances=substances_schema)
    return response



@router.get('/{id}')
async def get_substance_by_id(
    id: int,
    session: session_dependency,
) -> schemas.SubstanceSchema:
    query = (select(SubstanceModel.id, SubstanceModel.name, UnitModel.symbol, SubstanceModel.mpc)
             
            .where(SubstanceModel.id == id)
            .join(UnitModel)
    )
    result = await session.execute(query)
    substance = result.first()

    if not substance:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Substances with ID: {id!r} does not exist!')
    substance_schema = schemas.SubstanceSchema(
        id=substance[0],
        name=substance[1],
        unit_symbol=substance[2],  
        mpc=substance[3]
    )
    return substance_schema