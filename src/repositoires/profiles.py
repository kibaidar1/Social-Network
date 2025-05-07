from src.db.models.profiles import Profile
from src.exeptions import ProfileAlreadyExistsException
from src.repositoires.base_repository import SQLAlchemyRepository


class ProfilesRepository(SQLAlchemyRepository):
    model = Profile
    model_name = 'Профиль'
    integrity_error_redirect = ProfileAlreadyExistsException
