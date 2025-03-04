from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy import select

from app.aecs import schemas
from app.models.database import session_dependency
from app.models.substances import SubstanceModel

router = APIRouter(prefix="/substance",tags=["Substance"])

@router.get('/all')
async def get_substances(
    session: session_dependency
) -> schemas.SubstanceListSchema:
    ...

@router.get('/{id}')
async def get_substance_by_id(
    id: int,
    session: session_dependency,
) -> schemas.SubstanceSchema:
    ...