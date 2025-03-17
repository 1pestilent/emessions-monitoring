
from typing import Annotated

from fastapi import Depends

from sqlalchemy.ext.asyncio import (AsyncAttrs, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.core.config import (DB_HOST, DB_NAME, DB_PASSWORD, DB_PORT, DB_USER)


engine = create_async_engine(f"postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

new_session = sessionmaker(
    engine,
    expire_on_commit=True,
    class_=AsyncSession
    )

async def get_session():
    async with new_session() as session:
        yield session

class Base(AsyncAttrs, DeclarativeBase):
    pass

async def setup_database():
    async with engine.begin() as con:
        await con.run_sync(Base.metadata.drop_all)
        await con.run_sync(Base.metadata.create_all)

    return {"Status": True, "Text": "База успешно создана!"}


session_dependency = Annotated[AsyncSession, Depends(get_session)]
