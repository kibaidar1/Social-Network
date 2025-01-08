from src.auth.schemas import UserReadAll
from src.utils.unitofwork import UnitOfWork


class UsersService:
    @staticmethod
    async def get_all_users(uow: UnitOfWork) -> list[UserReadAll]:
        async with uow:
            users = await uow.users.find_all()
            print(users)
            return [UserReadAll.model_validate(user) for user in users]



