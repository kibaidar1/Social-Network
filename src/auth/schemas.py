from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, BaseModel

from src.profile.schemas import ProfileRead


class UserReadAll(BaseModel):
    id: int
    username: str
    profile: ProfileRead | None

    model_config = ConfigDict(from_attributes=True)


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    profile: ProfileRead | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateUpdate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
