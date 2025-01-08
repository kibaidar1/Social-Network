from src.db.models.profiles import Profile
from src.repositoires.base_repository import SQLAlchemyRepository


class ProfilesRepository(SQLAlchemyRepository):
    model = Profile
