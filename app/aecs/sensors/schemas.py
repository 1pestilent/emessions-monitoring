from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class AddSensorSchema(BaseModel):
    name: str
    serial_number: str
    unit_id: int
    description: str | None
    status: int

class ChangeSensorSchema(BaseModel):
    model_config = ConfigDict()

    name: Optional[str] = None
    serial_number: Optional[str] = None
    unit_id: Optional[int] = None
    description: Optional[str] = None
    status: Optional[int] = None

class SensorSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    serial_number: str
    unit_id: int
    installation_date: datetime | None = None
    calibration_date: datetime | None = None
    description: str
    status: int

class SensorViewSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    serial_number: str
    unit_symbol: str
    installation_date: datetime | None = None
    calibration_date: datetime | None = None
    description: str
    status_name: str

class SensorViewListSchema(BaseModel):
    sensors: List[SensorViewSchema]

class AddSensorReadingsSchema(BaseModel):
    sensor_id: int
    value: float

class ReadingsSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sensor_id: int
    value: float
    timestamp: datetime

class ReadingListSchema(BaseModel):
    readings: List[ReadingsSchema]

class ResponseAverageReadingSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    sensor_id: int
    value: float