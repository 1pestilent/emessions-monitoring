from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select

from app.core import dictionary
from app.models.aecs import StatusModel, SubstanceModel, UnitModel
from app.models.database import session_dependency, setup_database

router = APIRouter(prefix="/aecs/create",tags=["CREATE"])

@router.get('/database')
async def setup_db():
    return await setup_database()

@router.get('/all')
async def create_all(
    session: session_dependency,
):
    responses = []
    
    try:
        status_response = await create_statuses(session)
        responses.append(status_response)
    except HTTPException as e:
        responses.append({"status_code": e.status_code, "detail": e.detail})
    
    try:
        units_response = await create_units(session)
        responses.append(units_response)
    except HTTPException as e:
        responses.append({"status_code": e.status_code, "detail": e.detail})
    
    try:
        substances_response = await create_substances(session)
        responses.append(substances_response)
    except HTTPException as e:
        responses.append({"status_code": e.status_code, "detail": e.detail})
    
    return responses

@router.get('/statuses')
async def create_statuses(
    session: session_dependency,
):
    k = 0
    for sensor_status in dictionary.statuses:
        result = await session.execute(select(StatusModel).where(StatusModel.id == sensor_status['id']))
        existing_status = result.scalars().first()

        if not existing_status:
            sensor_status = StatusModel(**sensor_status)
            session.add(sensor_status)

        else:
            k += 1
        
    if k:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{k} of {len(dictionary.statuses)} statuses is already created! ')
    await session.commit()
    return {"status_code": status.HTTP_200_OK, "message": "Statuses successfully created."}

@router.get('/units')
async def create_units(
    session: session_dependency,
):
    k = 0
    for unit in dictionary.units:
        result = await session.execute(select(UnitModel).where(UnitModel.id == unit['id']))
        existing_unit = result.scalars().first()

        if not existing_unit:
            unit = UnitModel(**unit)
            session.add(unit)
        else:
            k += 1

    if k:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{k} of {len(dictionary.units)} units is already created! ')

    await session.commit()
    return {"status_code": status.HTTP_200_OK, "message": "Units successfully created."}

@router.get('/substances')
async def create_substances(
    session: session_dependency,
):
    k = 0
    for substance in dictionary.substances:
        result = await session.execute(select(SubstanceModel).where(SubstanceModel.id == substance['id']))
        existing_substance = result.scalars().first()

        if not existing_substance:
            substance = SubstanceModel(**substance)
            session.add(substance)
        else:
            k += 1

    if k:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'{k} of {len(dictionary.substances)} substances is already created! ')

    await session.commit()
    return {"status_code": status.HTTP_200_OK, "message": "Substances successfully created."}

    
