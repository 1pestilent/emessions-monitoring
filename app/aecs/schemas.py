from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class StatusSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str

class StatusListSchema(BaseModel):
    statuses: List[StatusSchema]

class SubstanceSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    unit: int
    mpc: float

class UnitSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    symbol: str

class UnitListSchema(BaseModel):
    units: List[UnitSchema]

class SubstanceSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    unit_symbol: str
    mpc: float | None

class SubstanceListSchema(BaseModel):
    substances: List[SubstanceSchema]