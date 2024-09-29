import datetime
from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: str
    data: Any or None = None
    errors: Any or None = None
    meta: Any or None = None


class AssistantRead(BaseModel):
    name: str
    mission_description: str
    task_description: str
    created_at: datetime.datetime

    class Config:
        from_attributes = True


class AssistantCreate(BaseModel):
    name: str
    mission_description: str
    task_description: str



