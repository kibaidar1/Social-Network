from abc import abstractmethod, ABCMeta

from sqlalchemy import select, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(metaclass=ABCMeta):
    model = None

    @abstractmethod
    async def add_one(self, values: dict):
        ...

    async def edit_one(self, id: int, data: dict):
        ...

    @abstractmethod
    async def find_all(self):
        ...


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, values: dict, returning: str = 'id') -> int:
        stmt = insert(self.model).values(**values).returning(getattr(self.model, returning))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def delete_one(self, **filter_by) -> bool:
        stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        await self.session.commit()
        return True if res.rowcount else False

    async def edit_one(self, values: dict, returning: str = 'id', **filter_by) -> int:
        stmt = (update(self.model)
                .filter_by(**filter_by)
                .values(**values)
                .returning(getattr(self.model, returning)))
        res = await self.session.execute(stmt)
        return res.scalar_one()

    async def get_by_id(self, id: int) -> dict or None:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        return res.scalar_one() if res else None

    async def find_all(self, **filter_by) -> list[dict] or None:
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.unique().scalars().all() if res else None

    async def find_one(self, **filter_by) -> dict or None:
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.unique().scalar_one() if res else None







