from typing import List

from pydantic import BaseModel, ConfigDict


class SubstanceSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    unit: int
    mpc: float

class SubstanceSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    unit_symbol: str
    mpc: float | None

class SubstanceListSchema(BaseModel):
    substances: List[SubstanceSchema]