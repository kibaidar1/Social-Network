from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey

from src.db.database import Base


class Profile(Base):
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id", ondelete="CASCADE"), unique=True)
    user: Mapped["User"] = relationship("User",
                                        back_populates='profile',
                                        uselist=False)
    name: Mapped[str]
    surname: Mapped[str]
    photo_url: Mapped[String] = mapped_column(String, nullable=True)

    def __str__(self):
        return f'{self.surname} {self.name}'
