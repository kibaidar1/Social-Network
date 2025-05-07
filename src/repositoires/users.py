from src.db.models.users import User
from src.exeptions import UserEmailAlreadyRegisteredException
from src.repositoires.base_repository import SQLAlchemyRepository


class UsersRepository(SQLAlchemyRepository):
    model = User
    model_name = 'Пользователь'
    integrity_error_redirect = UserEmailAlreadyRegisteredException
