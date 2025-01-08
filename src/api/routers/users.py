from fastapi import APIRouter, Depends


from src.api.auth_config import fastapi_users
from src.api.dependencies import UOWDep
from src.base_schema import async_base_crud_route
from src.schemas.users import UserRead, UserCreateUpdate
from src.services.users import UsersService

router = APIRouter(prefix="/users",
                   tags=["users"])
router.include_router(fastapi_users.get_users_router(UserRead, UserCreateUpdate))


@router.get("")
@async_base_crud_route(200)
async def get_users(uow: UOWDep):
    users = await UsersService.get_all_users(uow)
    return users









