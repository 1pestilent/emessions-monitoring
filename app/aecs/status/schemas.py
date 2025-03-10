from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class StatusSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str

class StatusListSchema(BaseModel):
    statuses: List[StatusSchema]
