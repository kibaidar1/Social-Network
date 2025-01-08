from sqlalchemy import Integer, ForeignKey
from sqlalchemy.orm import Mapped, relationship, mapped_column, validates

from src.db.database import Base


class Comment(Base):
    text: Mapped[str]
    post_id: Mapped[int] = mapped_column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    post: Mapped["Post"] = relationship("Post",
                                        back_populates="comments",
                                        lazy='joined')
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user: Mapped["User"] = relationship("User",
                                        back_populates="comments",
                                        lazy='joined')

    def __str__(self):
        return f'Comment by {self.user} on {self.post}'
