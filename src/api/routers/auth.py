from typing import Tuple

from fastapi import APIRouter, Request, Depends, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, models, exceptions, schemas
from fastapi_users.authentication import Strategy, Authenticator
from pydantic import EmailStr
from starlette import status


from src.api.auth_config import fastapi_users, auth_backend
from src.api.base_route_schema import BaseResponse
from src.api.user_manager import get_user_manager
from src.schemas.users import UserRead, UserCreateUpdate

router = APIRouter(prefix="/auth/jwt",
                   tags=["auth"])

# router.include_router(fastapi_users.get_auth_router(auth_backend))
# router.include_router(fastapi_users.get_register_router(UserRead, UserCreateUpdate))
router.include_router(fastapi_users.get_reset_password_router())
# router.include_router(fastapi_users.get_verify_router(UserRead))


get_current_user_token = fastapi_users.authenticator.current_user_token(
    active=True, verified=False
)


@router.post("/login",
             name=f"auth:{auth_backend.name}.login")
async def login(
    request: Request,
    credentials: OAuth2PasswordRequestForm = Depends(),
    user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager),
    strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy),
):
    user = await user_manager.authenticate(credentials)

    if user is None or not user.is_active:
        raise exceptions.InvalidPasswordException(None)
    response = await auth_backend.login(strategy, user)
    await user_manager.on_after_login(user, request, response)
    return response


@router.post("/logout",
             name=f"auth:{auth_backend.name}.logout")
async def logout(user_token: Tuple[models.UP, str] = Depends(get_current_user_token),
                 strategy: Strategy[models.UP, models.ID] = Depends(auth_backend.get_strategy)):
    user, token = user_token
    return await auth_backend.logout(strategy, user, token)


@router.post("/register",
             response_model=BaseResponse,
             status_code=status.HTTP_201_CREATED,
             name="register:register")
async def register(request: Request,
                   user_create: UserCreateUpdate,
                   user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager)):
    created_user = await user_manager.create(
        user_create, safe=True, request=request)
    valid_created_user = UserRead.model_validate(created_user)
    return BaseResponse(data=valid_created_user.model_dump())


@router.post(
        "/forgot-password",
        status_code=status.HTTP_202_ACCEPTED,
        name="reset:forgot_password")
async def forgot_password(request: Request,
                          email: EmailStr = Body(..., embed=True),
                          user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager)):
    user = await user_manager.get_by_email(email)
    await user_manager.forgot_password(user, request)


@router.post("/reset-password",
             name="reset:reset_password")
async def reset_password(request: Request,
                         token: str = Body(...),
                         password: str = Body(...),
                         user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager)):
    await user_manager.reset_password(token, password, request)


@router.post("/request-verify-token",
             status_code=status.HTTP_202_ACCEPTED,
             name="verify:request-token")
async def request_verify_token(request: Request,
                               email: EmailStr = Body(..., embed=True),
                               user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager)):
    user = await user_manager.get_by_email(email)
    await user_manager.request_verify(user, request)
    return None


@router.post("/verify", response_model=BaseResponse, name="verify:verify")
async def verify(request: Request,
                 token: str = Body(..., embed=True),
                 user_manager: BaseUserManager[models.UP, models.ID] = Depends(get_user_manager)):
    user = await user_manager.verify(token, request)
    valid_user = UserRead.model_validate(user)
    return BaseResponse(message='ОК', data=valid_user.model_dump())

