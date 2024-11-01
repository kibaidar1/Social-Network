from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.orm import Session

from src.auth.base_config import auth_backend, current_active_user, fastapi_users
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreateUpdate
from src.database import get_async_session

router = APIRouter()


router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreateUpdate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserCreateUpdate),
    prefix="/users",
    tags=["users"],
)

