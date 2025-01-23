from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import ForeignKey

from dotenv import load_dotenv
import os

engine = create_async_engine(f"postgresql+asyncpg://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}")

new_session = async_sessionmaker(engine, expire_on_commit=True)

async def get_session():
    async with new_session() as session:
        yield session



class Base(DeclarativeBase):
    pass

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

