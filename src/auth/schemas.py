from typing import Optional

from fastapi_users import schemas
from pydantic import EmailStr, BaseModel, Json, ConfigDict


class UserRead(schemas.BaseUser[int]):
    id: int
    username: str
    email: EmailStr
    role: int
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    model_config = ConfigDict(from_attributes=True)


class UserCreateUpdate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False


class RoleCreate(BaseModel):
    name: str
    permission: str
