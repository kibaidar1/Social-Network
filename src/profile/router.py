

from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from functools import wraps

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.auth.base_config import current_active_user
from src.auth.models import User
from src.base_schema import BaseResponse
from src.database import get_async_session
from src.profile.models import Profile
from src.profile.schemas import ProfileCreateUpdate, ProfileRead

router = APIRouter(prefix='/profile',
                   tags=['profile'])


def async_base_route(success_status):
    def decorator(rout):
        @wraps(rout)
        async def wrapper(*args, **kwargs):
            status_code = success_status
            message = 'Success'
            data = []
            errors = []

            try:
                result = await rout(*args, **kwargs)
                if result:
                    data.append(result)

            except NoResultFound as e:
                print(e)
                message = 'Failed'
                status_code = 404
                errors.append('Profile is not exists')

            except IntegrityError as e:
                print(e)
                message = 'Failed'
                status_code = 400
                errors.append("Profile already exists")

            except Exception as e:
                print(e)
                message = "Failed"
                status_code = 500
                errors.append('Unknown error')

            finally:
                return JSONResponse(status_code=status_code,
                                    content=BaseResponse(
                                        message=message,
                                        data=data,
                                        errors=errors,
                                    ).model_dump())
        return wrapper
    return decorator



@router.post("/", response_model=BaseResponse)
@async_base_route(success_status=201)
async def create_profile(profile: ProfileCreateUpdate,
                         session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    stmt = insert(Profile).values(**profile.model_dump(), user_id=user.id)
    await session.execute(stmt)
    await session.commit()
    return profile


@router.get("/", response_model=BaseResponse)
@async_base_route(success_status=200)
async def get_profile(session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):

    query = (select(Profile)
             .where(Profile.user_id == user.id))
    profile = await session.execute(query)
    profile_data = ProfileRead.model_validate(profile.scalar_one(), from_attributes=True)
    return profile_data


@router.put("/", response_model=BaseResponse)
@async_base_route(success_status=200)
async def update_profile(profile: ProfileCreateUpdate, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):

    stmt = (update(Profile)
            .where(Profile.user_id == user.id)
            .values(**profile.model_dump(), user_id=user.id))
    result = await session.execute(stmt)
    if not result.rowcount:
        raise NoResultFound
    await session.commit()
    return profile


@router.delete("/", response_model=BaseResponse)
@async_base_route(success_status=200)
async def delete_profile(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):

    stmt = (delete(Profile)
            .where(Profile.user_id == user.id))
    result = await session.execute(stmt)
    if not result.rowcount:
        raise NoResultFound
    await session.commit()



