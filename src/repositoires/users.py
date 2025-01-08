from src.db.models.users import User
from src.repositoires.base_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
