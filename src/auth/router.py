from fastapi import APIRouter, Depends
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import auth_backend, current_active_user, fastapi_users
from src.auth.models import User
from src.auth.schemas import UserRead, UserCreateUpdate, UserReadAll
from src.base_schema import async_base_crud_route
from src.database import get_async_session


auth_router = APIRouter(prefix="/auth/jwt",
                        tags=["auth"])

auth_router.include_router(fastapi_users.get_auth_router(auth_backend))
auth_router.include_router(fastapi_users.get_register_router(UserRead, UserCreateUpdate))
auth_router.include_router(fastapi_users.get_reset_password_router())
auth_router.include_router(fastapi_users.get_verify_router(UserRead))


users_router = APIRouter(prefix="/users",
                         tags=["users"])
users_router.include_router(fastapi_users.get_users_router(UserRead, UserCreateUpdate))


@users_router.get("/")
@async_base_crud_route(200)
async def get_users(session: AsyncSession = Depends(get_async_session),
                    _: User = Depends(current_active_user)):
    stmt = select(User)
    data = await session.execute(stmt)
    users = [UserReadAll.model_validate(u, from_attributes=True) for u in data.scalars().all()]
    return users







