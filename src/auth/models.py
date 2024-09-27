from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class Role(Base):
    __tablename__ = "roles"
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, unique=True)
    permission: Mapped[JSON] = mapped_column(JSON, nullable=True)


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(String)
    role: Mapped[ForeignKey] = mapped_column(ForeignKey(Role.id))
    registered_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now())
