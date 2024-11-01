from datetime import datetime

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str]
    registered_at: Mapped[TIMESTAMP] = mapped_column(TIMESTAMP, default=datetime.now())
    profile: Mapped["Profile"] = relationship("Profile",
                                              back_populates="user",
                                              uselist=False)
