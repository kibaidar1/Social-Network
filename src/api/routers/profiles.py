from fastapi import APIRouter, Depends, UploadFile, File
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import RedirectResponse

from starlette import status

from src.api.auth_config import current_active_user
from src.api.base_route_schema import async_base_crud_route
from src.api.dependencies import UOWDep
from src.base_schema import BaseResponse
from src.db.models.users import User
from src.schemas.profiles import Profile
from src.services.profiles import ProfilesService

router = APIRouter(prefix='/profile',
                   tags=['profile'])


@router.get("/", response_model=BaseResponse)
@async_base_crud_route(success_status=200)
async def get_profile(uow: UOWDep,
                      user: User = Depends(current_active_user)):
    profile = await ProfilesService.get_profile(uow, user)
    return profile


GET_PROFILE_URL = router.url_path_for(str(get_profile.__name__))


@router.post("/", response_model=BaseResponse)
async def create_profile(uow: UOWDep,
                         profile: Profile,
                         user: User = Depends(current_active_user)):
    profile_id = await ProfilesService.create_profile(uow, profile, user)
    return RedirectResponse(GET_PROFILE_URL, status_code=status.HTTP_303_SEE_OTHER)


@router.patch("/", response_model=BaseResponse)
async def update_profile(uow: UOWDep,
                         profile: Profile,
                         user: User = Depends(current_active_user)):
    profile_id = await ProfilesService.update_profile(uow, profile, user)
    url = router.url_path_for(str(get_profile.__name__))
    return RedirectResponse(GET_PROFILE_URL, status_code=status.HTTP_303_SEE_OTHER)


@router.delete("/", response_model=BaseResponse)
@async_base_crud_route(success_status=200)
async def delete_profile(uow: UOWDep,
                         user: User = Depends(current_active_user)):
    await ProfilesService.delete_profile(uow, user)
    return []


@router.post('/add_photo', response_model=BaseResponse)
async def add_photo(uow: UOWDep,
                    file: UploadFile = File(..., description="Загрузите изображение в формате JPG или PNG"),
                    user: User = Depends(current_active_user)):
    profile_id = await ProfilesService.add_photo(uow, user, file)
    return RedirectResponse(GET_PROFILE_URL, status_code=status.HTTP_303_SEE_OTHER)
