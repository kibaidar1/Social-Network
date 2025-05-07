from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status

from src.api.auth_config import current_active_user
from src.api.base_route_schema import BaseResponse
from src.api.dependencies import UOWDep
from src.db.models.users import User
from src.schemas.comments import CommentCreateUpdate
from src.services.comments import CommentService

router = APIRouter(prefix='/posts',
                   tags=['comments'])


@router.post('/{post_slug}',
             status_code=status.HTTP_201_CREATED,
             response_model=BaseResponse)
async def add_comment(uow: UOWDep,
                      post_slug: str,
                      comment: CommentCreateUpdate,
                      user: User = Depends(current_active_user)):
    comment_id = await CommentService.create_comment(uow, comment, post_slug, user.id)
    return BaseResponse(message='Комментарий создан',
                        data={'comment_id': comment_id})



