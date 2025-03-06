from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

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

class AddSensorSchema(BaseModel):
    name: str
    serial_number: str
    unit_id: int
    description: str | None
    status: int

class InstallationSensorSchema(BaseModel):
    id: str | None 
    serial_number: str | None
    installation_date: datetime

class CalibrationSensorSchema(BaseModel):
    id: str | None 
    serial_number: str | None
    calibration_date: datetime

class SensorSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)

    id: int
    name: str
    serial_number: str
    unit_symbol: str
    installation_date: datetime | None = None
    calibration_date: datetime | None = None
    description: str
    status_name: str