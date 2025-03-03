from pydantic import BaseModel, ConfigDict
from typing import List

class StatusSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str

class StatusesSchema(BaseModel):
    statuses: List[StatusSchema]