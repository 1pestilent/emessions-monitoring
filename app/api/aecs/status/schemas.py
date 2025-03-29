from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class StatusSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str

class StatusListSchema(BaseModel):
    statuses: List[StatusSchema]
