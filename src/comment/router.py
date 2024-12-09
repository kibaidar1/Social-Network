from fastapi import Depends
from fastapi.routing import APIRouter
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.base_config import current_active_user
from src.auth.models import User
from src.base_schema import async_base_crud_route
from src.comment.models import Comment
from src.comment.schemas import CommentCreateUpdate
from src.database import get_async_session
from src.post.models import Post

router = APIRouter(prefix='/posts',
                   tags=['posts'])


@router.post('/{post_slug}')
@async_base_crud_route(201)
async def add_comment(post_slug: str,
                      comment: CommentCreateUpdate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    stmt = select(Post).where(Post.slug == post_slug)
    res = await session.execute(stmt)
    post = res.unique().scalar_one()
    stmt = (insert(Comment).values(post_id=post.id, user_id=user.id, text=comment.text))
    await session.execute(stmt)
    await session.commit()
    return comment



