from src.database import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, String, ForeignKey


class Profile(Base):
    __tablename__ = 'profile'
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    user: Mapped["User"] = relationship("User",
                                        back_populates='profile',
                                        uselist=False)
    name: Mapped[str]
    surname: Mapped[str]
    photo: Mapped[String] = mapped_column(String, nullable=True)

