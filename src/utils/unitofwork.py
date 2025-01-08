from typing import Type

from src.database import async_session_maker
from src.repositoires.comments import CommentsRepository
from src.repositoires.posts import PostsRepository
from src.repositoires.profiles import ProfilesRepository
from src.repositoires.users import UsersRepository


class IUnitOfWork:
    users: Type[UsersRepository]
    profiles: Type[ProfilesRepository]
    posts: Type[PostsRepository]
    comments: Type[CommentsRepository]

    def __init__(self):
        ...

    async def __aenter__(self):
        ...

    async def __aexit__(self, *arfs):
        ...

    async def commit(self):
        ...

    async def rollback(self):
        ...


class UnitOfWork:

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.profiles = ProfilesRepository(self.session)
        self.posts = PostsRepository(self.session)
        self.comments = CommentsRepository(self.session)

    async def __aexit__(self, *arfs):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
