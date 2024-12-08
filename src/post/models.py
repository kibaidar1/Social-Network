from typing import List

from slugify import slugify
from sqlalchemy import Integer, ForeignKey, String, ARRAY, event
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from src.database import Base


class Post(Base):
    title: Mapped[str]
    text: Mapped[str]
    slug: Mapped[str] = mapped_column(String, unique=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User",
                                        back_populates="posts",
                                        lazy='joined')
    comments: Mapped["List[Comment]"] = relationship("Comment",
                                                     back_populates="post",
                                                     lazy='joined')

    def __str__(self):
        return self.slug


class Comment(Base):
    text: Mapped[str]
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id"))
    post: Mapped["Post"] = relationship("Post", back_populates="comments")
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    user: Mapped["User"] = relationship("User",
                                        back_populates="comments",
                                        lazy='joined')

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post.slug}"



