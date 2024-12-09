from typing import List
from sqlalchemy import Integer, ForeignKey, String, ARRAY, event
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from src.database import Base


class Post(Base):
    title: Mapped[str]
    text: Mapped[str]
    slug: Mapped[str] = mapped_column(String, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User",
                                        back_populates="posts",
                                        lazy='joined')
    comments: Mapped[List["Comment"]] = relationship("Comment",
                                                     back_populates="post",
                                                     lazy='joined',
                                                     uselist=True,
                                                     cascade='all, delete-orphan')

    def __str__(self):
        return self.slug




