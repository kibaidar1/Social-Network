from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict

from src.profile.schemas import ProfileRead


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
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
