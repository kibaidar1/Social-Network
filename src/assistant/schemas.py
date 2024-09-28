import datetime

from pydantic import BaseModel


class AssistantRead(BaseModel):
    name: str
    mission_description: str
    task_description: str
    created_at: datetime.datetime

    class Config:
        orm_mode = True


class AssistantCreate(BaseModel):
    name: str
    mission_description: str
    task_description: str



