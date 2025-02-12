from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.database import Base

class UnitModel(Base):
    __tablename__ = 'units'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    symbol: Mapped[str]
    

class SubstanceModel(Base):
    __tablename__ = "substances"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    unit_id: Mapped[int] = mapped_column(ForeignKey('units.id',ondelete='RESTRICT'))
    mpc: Mapped[float]
