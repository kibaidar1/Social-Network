from sqlalchemy import select

from src.db.models.posts import Post
from src.exeptions import EntityNotFoundException
from src.repositoires.base_repository import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = Post
    model_name = 'Пост'

    async def find_post_with_slug_like(self, like):
        query = select(self.model).filter(self.model.slug.like(like))
        res = await self.session.execute(query)
        obj = res.unique().scalars().all() if res else None
        if not obj:
            raise EntityNotFoundException(self.model_name)
        return obj




