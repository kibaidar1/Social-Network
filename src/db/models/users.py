from typing import List

from fastapi_users_db_sqlalchemy import SQLAlchemyBaseUserTable
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.database import Base


class User(SQLAlchemyBaseUserTable[int], Base):
    username: Mapped[str]
    profile: Mapped["Profile"] = relationship("Profile",
                                              back_populates="user",
                                              uselist=False,
                                              lazy='joined',
                                              cascade='all, delete-orphan')
    posts: Mapped[List["Post"]] = relationship("Post",
                                               back_populates='user',
                                               uselist=True,
                                               lazy='joined',
                                               cascade='all, delete-orphan')
    comments: Mapped[List["Comment"]] = relationship("Comment",
                                                     back_populates='user',
                                                     uselist=True,
                                                     lazy='joined',
                                                     cascade='all, delete-orphan')

    def __str__(self):
        return self.username
