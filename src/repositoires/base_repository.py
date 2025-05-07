from abc import abstractmethod, ABCMeta

from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.database import Base
from src.exeptions import UnknownException, EntityNotFoundException


class AbstractRepository(metaclass=ABCMeta):
    model = None

    @abstractmethod
    async def add_one(self, values: dict):
        ...

    @abstractmethod
    async def edit_one(self, id: int, data: dict):
        ...

    @abstractmethod
    async def find_all(self):
        ...


class SQLAlchemyRepository(AbstractRepository):
    model: Base = None
    model_name: str = model.__name__ if model else None
    integrity_error_redirect: Exception = UnknownException

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, values: dict, returning: str = 'id') -> int:
        try:
            stmt = (insert(self.model)
                    .values(**values).returning(getattr(self.model, returning)))
            res = await self.session.execute(stmt)
            return res.scalar_one()
        except IntegrityError as e:
            raise self.integrity_error_redirect

    async def delete_one(self, **filter_by) -> bool:
        stmt = delete(self.model).filter_by(**filter_by)
        res = await self.session.execute(stmt)
        if res.rowcount == 0:
            raise EntityNotFoundException(self.model_name)
        return True

    async def edit_one(self, values: dict, returning: str = 'id', **filter_by) -> int:
        stmt = (update(self.model)
                .filter_by(**filter_by)
                .values(**values)
                .returning(getattr(self.model, returning)))
        res = await self.session.execute(stmt)
        obj = res.scalar_one_or_none()
        if not obj:
            raise EntityNotFoundException(self.model_name)
        return obj

    async def get_by_id(self, id: int) -> dict or None:
        stmt = select(self.model).where(self.model.id == id)
        res = await self.session.execute(stmt)
        obj = res.scalar_one_or_none()
        if not obj:
            raise EntityNotFoundException(self.model_name)
        return obj

    async def find_all(self, **filter_by) -> list[dict] or None:
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        return res.unique().scalars().all() if res else None

    async def find_one(self, **filter_by) -> dict or None:
        query = select(self.model).filter_by(**filter_by)
        res = await self.session.execute(query)
        obj = res.unique().scalar_one_or_none()
        if not obj:
            raise EntityNotFoundException(self.model_name)
        return obj







