from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class UnitSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    symbol: str

class UnitListSchema(BaseModel):
    units: List[UnitSchema]
