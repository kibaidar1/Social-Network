from fastapi import APIRouter

from src.api.auth_config import fastapi_users, auth_backend
from src.schemas.users import UserRead, UserCreateUpdate

router = APIRouter(prefix="/auth/jwt",
                   tags=["auth"])

router.include_router(fastapi_users.get_auth_router(auth_backend))
router.include_router(fastapi_users.get_register_router(UserRead, UserCreateUpdate))
router.include_router(fastapi_users.get_reset_password_router())
router.include_router(fastapi_users.get_verify_router(UserRead))
