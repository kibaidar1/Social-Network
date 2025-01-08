from src.post.schemas import PostRead
from src.schemas.posts import PostCreate, PostUpdate, PostReadDetail
from src.services.utils import generate_unique_slug
from src.utils.unitofwork import UnitOfWork


class PostsService:

    @staticmethod
    async def add_post(uow: UnitOfWork,
                       post: PostCreate,
                       user_id: int) -> str:
        slug = await generate_unique_slug(uow, post.title)
        values = {**post.model_dump(), 'user_id': user_id, 'slug': slug}
        async with uow:
            post_slug = await uow.posts.add_one(values, returning='slug')
            await uow.commit()
            return post_slug

    @staticmethod
    async def delete_post(uow: UnitOfWork,
                          slug: str,
                          user_id: int) -> bool:
        async with uow:
            res = await uow.posts.delete_one(slug=slug, user_id=user_id)
            await uow.commit()
            return True if res > 0 else False

    @staticmethod
    async def edit_post(uow: UnitOfWork,
                        slug: str,
                        post: PostUpdate,
                        user_id: int) -> str:
        values = {**post.model_dump(), 'user_id': user_id, }
        async with uow:
            post_slug = await uow.posts.edit_one(values=post.model_dump(),
                                                 slug=slug,
                                                 user_id=user_id,
                                                 returning='slug')
            await uow.commit()
            return post_slug

    @staticmethod
    async def find_posts(uow: UnitOfWork,
                         filter_by) -> list:
        async with uow:
            posts = await uow.posts.find_all()
            return posts

    @staticmethod
    async def get_all_posts(uow: UnitOfWork) -> list[PostRead]:
        async with uow:
            posts = await uow.posts.find_all()
            return [PostRead.model_validate(post) for post in posts]

    @staticmethod
    async def get_post_detail(uow: UnitOfWork,
                              slug: str) -> PostReadDetail:
        async with uow:
            post = await uow.posts.find_one(slug=slug)
            return PostReadDetail.model_validate(post) if post else None

    @staticmethod
    async def get_user_posts(uow: UnitOfWork, user_id: int) -> list[PostRead]:
        async with uow:
            posts = await uow.posts.find_all(user_id=user_id)
            return [PostRead.model_validate(post) for post in posts]





