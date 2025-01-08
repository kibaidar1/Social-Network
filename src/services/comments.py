from src.schemas.comments import CommentCreateUpdate
from src.utils.unitofwork import UnitOfWork


class CommentService:

    @staticmethod
    async def create_comment(uow: UnitOfWork,
                             comment: CommentCreateUpdate,
                             post_slug: str,
                             user_id: int) -> int:
        async with uow:
            post = await uow.posts.find_one(slug=post_slug)
            values = {**comment.model_dump(), 'post_id': post.id, 'user_id': user_id}
            comment_id = await uow.comments.add_one(values)
            await uow.commit()
            return comment_id
