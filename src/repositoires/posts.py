from sqlalchemy import select

from src.db.models.posts import Post
from src.repositoires.base_repository import SQLAlchemyRepository


class PostsRepository(SQLAlchemyRepository):
    model = Post

    async def find_post_with_slug_like(self, like):
        query = select(self.model).filter(self.model.slug.like(like))
        res = await self.session.execute(query)
        return res.unique().scalars().all() if res else None




