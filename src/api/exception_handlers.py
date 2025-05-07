from urllib.request import Request

from fastapi import FastAPI
from fastapi_users import InvalidPasswordException
from fastapi_users.exceptions import UserAlreadyExists, UserNotExists, UserInactive, InvalidResetPasswordToken, \
    UserAlreadyVerified, InvalidVerifyToken, InvalidID
from starlette import status
from starlette.responses import JSONResponse

from src.api.base_route_schema import BaseResponse
from src.exeptions import UserEmailAlreadyRegisteredException, ProfileAlreadyExistsException, EntityNotFoundException, \
    UnknownException


def init_exception_handlers(app: FastAPI):

    @app.exception_handler(ProfileAlreadyExistsException)
    async def profile_already_exists_exc_handler(request: Request,
                                                 exc: ProfileAlreadyExistsException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=BaseResponse(
                                        message=exc.__str__(),
                                    ).model_dump())

    @app.exception_handler(UserEmailAlreadyRegisteredException)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: UserEmailAlreadyRegisteredException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=BaseResponse(
                                message=exc.__str__(),
                            ).model_dump())

    @app.exception_handler(EntityNotFoundException)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: EntityNotFoundException):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message=exc.__str__(),
                            ).model_dump())

    @app.exception_handler(UnknownException)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: UnknownException):
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            content=BaseResponse(
                                message=exc.__str__(),
                            ).model_dump())

    """
    Fastapi-users exceptions
    """

    @app.exception_handler(InvalidPasswordException)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: InvalidPasswordException):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=BaseResponse(
                                message='Неверный логин или пароль.',
                            ).model_dump())

    @app.exception_handler(UserAlreadyExists)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: UserAlreadyExists):
        return JSONResponse(status_code=status.HTTP_400_BAD_REQUEST,
                            content=BaseResponse(
                                message='Пользователь с таким email уже зарегистрирован.',
                            ).model_dump())

    @app.exception_handler(InvalidID)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: InvalidID):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message='Пользователь не найден.',
                            ).model_dump())

    @app.exception_handler(UserNotExists)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: UserNotExists):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message='Пользователь с таким email не найден.',
                            ).model_dump())

    @app.exception_handler(UserInactive)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: UserInactive):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message='Пользователь с таким email не найден.',
                            ).model_dump())

    @app.exception_handler(InvalidResetPasswordToken)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: InvalidResetPasswordToken):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message='Неверный Токен.',
                            ).model_dump())

    @app.exception_handler(UserAlreadyVerified)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: UserAlreadyVerified):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message='Пользователь уже верифицирован.',
                            ).model_dump())

    @app.exception_handler(InvalidVerifyToken)
    async def user_email_already_registered_exc_handler(request: Request,
                                                        exc: InvalidVerifyToken):
        return JSONResponse(status_code=status.HTTP_404_NOT_FOUND,
                            content=BaseResponse(
                                message='Неверный токен, пользователь не существует или не совпадает '
                                        'с адресом электронной почты, указанным для пользователя.',
                            ).model_dump())










