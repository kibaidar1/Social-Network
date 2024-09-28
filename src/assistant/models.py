from datetime import datetime

from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import DeclarativeBase

from src.database import Base


class Assistant(Base):
    __tablename__ = 'assistant'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    mission_description = Column(String, nullable=False)
    task_description = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now())



