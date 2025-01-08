from fastapi_users import schemas
from pydantic import EmailStr, ConfigDict, BaseModel

from src.schemas.profiles import Profile


class UserReadAll(BaseModel):
    username: str
    profile: Profile | None

    model_config = ConfigDict(from_attributes=True)


class UserRead(schemas.BaseUser[int]):
    username: str
    email: EmailStr
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False
    profile: Profile | None = None

    model_config = ConfigDict(from_attributes=True)


class UserCreateUpdate(schemas.BaseUserCreate):
    username: str
    email: EmailStr
    password: str
