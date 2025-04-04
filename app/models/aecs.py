from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, String, Text, text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base


class StatusModel(Base):
    __tablename__ = 'status'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(31), nullable=False, unique=True)

class UnitModel(Base):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(63), nullable=False, unique=True)
    symbol: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)

class SubstanceModel(Base):
    __tablename__ = 'substances'

    id: Mapped[int] = mapped_column(primary_key=True) 
    name: Mapped[str] = mapped_column(String(15), nullable=False, unique=True)
    unit: Mapped[int] = mapped_column(ForeignKey('units.id', ondelete='RESTRICT'))
    mpc: Mapped[float] = mapped_column(Float, nullable=True)
    
class SensorModel(Base):
    __tablename__ = 'sensors'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False)
    serial_number: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id', ondelete='RESTRICT'))
    installation_date: Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    calibration_date:  Mapped[DateTime] = mapped_column(DateTime, nullable=True)
    description: Mapped[Text] = mapped_column(Text)
    status: Mapped[int] = mapped_column(ForeignKey('status.id', ondelete='RESTRICT'), default = 1)

class SensorReadingsModel(Base):
    __tablename__ = 'readings'

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey('sensors.id', ondelete='RESTRICT'))
    value: Mapped[float] = mapped_column(Float)
    timestamp: Mapped[DateTime] = mapped_column(DateTime)

class LocationModel(Base):
    __tablename__ = 'locations'
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(127), nullable=False, unique=True)
    description: Mapped[Text] = mapped_column(Text)

class SensorMappingModel(Base):
    __tablename__ = 'sensors_mapping'

    id: Mapped[int] = mapped_column(primary_key=True)
    sensor_id: Mapped[int] = mapped_column(ForeignKey('sensors.id', ondelete='RESTRICT'))
    location_id: Mapped[int] = mapped_column(ForeignKey('locations.id', ondelete='RESTRICT'))