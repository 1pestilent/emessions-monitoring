from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, DateTime, text

from app.models.database import Base

class UserModel(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(63), unique=True, nullable=False)
    password: Mapped[bytes] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(String(31), nullable=False)
    first_name: Mapped[str] = mapped_column(String(31), nullable=False)
    middle_name: Mapped[str] = mapped_column(String(63), nullable=True)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"))
    updated_at: Mapped[DateTime] = mapped_column(DateTime, server_default=text("CURRENT_TIMESTAMP"), onupdate=text("CURRENT_TIMESTAMP"))
    is_active: Mapped[bool] = mapped_column(Boolean, default=False)