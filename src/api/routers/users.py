from fastapi import APIRouter, Depends, Request
from fastapi_users import models, BaseUserManager
from starlette import status

from src.api.auth_config import fastapi_users
from src.api.base_route_schema import BaseResponse
from src.api.dependencies import UOWDep
from src.api.user_manager import get_user_manager
from src.schemas.users import UserRead, UserCreateUpdate
from src.services.users import UsersService

router = APIRouter(prefix="/users",
                   tags=["users"])
# router.include_router(fastapi_users.get_users_router(UserRead, UserCreateUpdate))

get_current_active_user = fastapi_users.authenticator.current_user(
        active=True, verified=False)

get_current_superuser = fastapi_users.authenticator.current_user(
    active=True, verified=False, superuser=True)


@router.get("/",
            status_code=status.HTTP_200_OK,
            response_model=BaseResponse)
async def get_users(uow: UOWDep):
    users = await UsersService.get_all_users(uow)
    return BaseResponse(data=[u.model_dump() for u in users])


@router.get("/me",
            response_model=BaseResponse,
            name="users:current_user")
async def me(user: models.UP = Depends(get_current_active_user)):
    valid_user = UserRead.model_validate(user)
    return BaseResponse(data=valid_user.model_dump())


@router.patch("/me",
              response_model=BaseResponse,
              dependencies=[Depends(get_current_active_user)],
              name="users:patch_current_user")
async def update_me(request: Request,
                    user_update: UserCreateUpdate,
                    user: models.UP = Depends(get_current_active_user),
                    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager)):
    user = await user_manager.update(user_update,
                                     user, safe=True,
                                     request=request)
    valid_user = UserRead.model_validate(user)
    return BaseResponse(data=valid_user.model_dump())












