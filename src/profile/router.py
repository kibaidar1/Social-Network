
from pathlib import Path

from fastapi import APIRouter, Depends, UploadFile, File


from functools import wraps

from fastapi.responses import JSONResponse

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError, NoResultFound
from src.auth.base_config import current_active_user
from src.auth.models import User
from src.base_schema import BaseResponse
from src.database import get_async_session
from src.profile.models import Profile
from src.profile.schemas import ProfileCreateUpdate, ProfileRead
from PIL import Image

router = APIRouter(prefix='/profile',
                   tags=['profile'])

# Директория для сохранения загруженных фото
UPLOAD_DIR = Path('static/photos')
UPLOAD_DIR.mkdir(exist_ok=True)

# Поддерживаемые форматы изображений
ALLOWED_EXTENSIONS = ("png", "jpg", "jpeg")
MAX_FILE_SIZE = 2 * 1024 * 1024  # Ограничение на 2 МБ
TARGET_SIZE = (1024, 1024)  # Целевой размер изображения


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

            except HTTPException as e:
                print(e)
                message = 'Failed'
                status_code = 400
                errors.append(str(e.detail))

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
             .where(Profile.user == user))
    profile = await session.execute(query)
    profile_data = ProfileRead.model_validate(profile.scalar_one(), from_attributes=True)
    return profile_data


@router.put("/", response_model=BaseResponse)
@async_base_route(success_status=200)
async def update_profile(profile: ProfileCreateUpdate, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):

    stmt = (update(Profile)
            .where(Profile.user == user)
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
            .where(Profile.user == user))
    result = await session.execute(stmt)
    if not result.rowcount:
        raise NoResultFound
    await session.commit()


def validate_and_save_photo(file: UploadFile, filename: str):
    # Проверка расширения файла
    extension = file.filename.split(".")[-1].lower()
    if extension not in ALLOWED_EXTENSIONS:
        raise HTTPException(status_code=400, detail="Invalid file format")

        # Проверка размера файла
    file.file.seek(0, 2)  # Переход в конец файла для получения размера
    file_size = file.file.tell()
    file.file.seek(0)  # Возврат в начало файла для последующих операций
    if file_size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="The file is too big")

    # Проверка, что файл действительно является изображением
    try:
        image = Image.open(file.file)
        image.verify()  # Проверка целостности изображения
        image = Image.open(file.file)  # Переоткрываем для обработки
    except (IOError, SyntaxError):
        raise HTTPException(status_code=400, detail="The file is not a valid image")

    # Пропорциональное изменение размера с обрезкой
    image.thumbnail(TARGET_SIZE)
    if image.size != TARGET_SIZE:
        image = image.resize(TARGET_SIZE, Image.Resampling.LANCZOS)

    # Сохранение изображения в целевом формате
    image_path = f"{filename}.png"
    image.save(UPLOAD_DIR / image_path)

    return image_path


@router.post('/add_photo', response_model=BaseResponse)
@async_base_route(success_status=201)
async def add_photo(file: UploadFile = File(..., description="Загрузите изображение в формате JPG или PNG"),
                    session: AsyncSession = Depends(get_async_session),
                    user: User = Depends(current_active_user)):
    file_path = validate_and_save_photo(file, str(user.id))
    photo_url = f"http://localhost:8000/photos/{file_path}"
    stmt = (update(Profile)
            .where(Profile.user == user)
            .values(photo_url=photo_url))
    result = await session.execute(stmt)
    if not result.rowcount:
        raise NoResultFound
    await session.commit()
    return photo_url



