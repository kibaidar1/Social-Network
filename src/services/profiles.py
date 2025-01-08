from PIL import Image

from src.db.models.users import User
from src.profile.schemas import ProfileRead
from src.services.utils import validate_and_save_photo
from src.utils.unitofwork import UnitOfWork
from src.schemas.profiles import Profile


class ProfilesService:

    @staticmethod
    async def create_profile(uow: UnitOfWork,
                             profile: Profile,
                             user: User) -> int:
        async with uow:
            values = {**profile.model_dump(), 'user_id': user.id}
            profile_id = await uow.profiles.add_one(values)
            await uow.commit()
            return profile_id

    @staticmethod
    async def get_profile(uow: UnitOfWork,
                          user: User) -> ProfileRead:
        async with uow:
            profile = await uow.profiles.find_one(user=user)
            return ProfileRead.model_validate(profile)

    @staticmethod
    async def update_profile(uow: UnitOfWork,
                             profile: Profile,
                             user: User) -> int:
        async with uow:
            profile_id = await uow.profiles.edit_one(profile.model_dump(exclude_defaults=True), user=user)
            await uow.commit()
            return profile_id

    @staticmethod
    async def delete_profile(uow: UnitOfWork,
                             user: User) -> int:
        async with uow:
            res = await uow.profiles.delete_one(user=user)
            await uow.commit()
            return res

    @staticmethod
    async def add_photo(uow: UnitOfWork,
                        user: User,
                        image_file: Image) -> int:
        file_path = validate_and_save_photo(image_file, str(user.id))
        values = {'photo_url': f'/photos/{file_path}'}
        async with uow:
            profile_id = await uow.profiles.edit_one(values, user=user)
            await uow.commit()
            return profile_id



