from datetime import datetime
from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy import Integer, String, TIMESTAMP, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str]
    profile: Mapped["Profile"] = relationship("Profile",
                                              back_populates="user",
                                              uselist=False,
                                              lazy='joined')
    posts: Mapped[List["Post"]] = relationship("Post",
                                               back_populates='user')
    comments: Mapped[List["Comment"]] = relationship("Comment",
                                                     back_populates='user')

    def __str__(self):
        return self.username