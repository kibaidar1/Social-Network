from fastapi import Depends
from fastapi.routing import APIRouter

from src.api.auth_config import current_active_user
from src.api.dependencies import UOWDep
from src.base_schema import async_base_crud_route
from src.db.models.users import User
from src.schemas.comments import CommentCreateUpdate
from src.services.comments import CommentService

router = APIRouter(prefix='/posts',
                   tags=['comments'])


@router.post('/{post_slug}')
@async_base_crud_route(201)
async def add_comment(uow: UOWDep,
                      post_slug: str,
                      comment: CommentCreateUpdate,
                      user: User = Depends(current_active_user)):
    comment_id = await CommentService.create_comment(uow, comment, post_slug, user.id)
    return {'comment_id': comment_id}



