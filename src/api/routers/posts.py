from fastapi import Depends
from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import RedirectResponse

from src.api.auth_config import current_active_user
from src.api.base_route_schema import async_base_crud_route
from src.api.dependencies import UOWDep
from src.db.models.users import User
from src.schemas.posts import PostRead, PostUpdate, PostCreate
from src.services.posts import PostsService

router = APIRouter(prefix='/posts',
                   tags=['posts'])


@router.get('/')
@async_base_crud_route(200)
async def get_all_posts(uow: UOWDep):
    posts = await PostsService.get_all_posts(uow)
    return posts


@router.get('/my_posts')
@async_base_crud_route(200)
async def get_my_posts(uow: UOWDep,
                       user: User = Depends(current_active_user)):
    posts = await PostsService.get_user_posts(uow,  user_id=user.id)
    return posts


@router.get('/{post_slug}')
@async_base_crud_route(200)
async def get_post_detail(uow: UOWDep,
                          post_slug: str):
    post = await PostsService.get_post_detail(uow, post_slug)
    return post


@router.post('/')
async def create_post(uow: UOWDep,
                      post_data: PostCreate,
                      user: User = Depends(current_active_user)):
    post_slug = await PostsService.add_post(uow, post_data, user_id=user.id)
    url = router.url_path_for(get_post_detail.__name__, post_slug=post_slug)
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@router.patch('/{post_slug}')
async def update_post(uow: UOWDep,
                      post_slug: str,
                      post_data: PostUpdate,
                      user: User = Depends(current_active_user)):
    post_slug = await PostsService.edit_post(uow, post_slug, post_data,  user_id=user.id)
    url = router.url_path_for(get_post_detail.__name__, post_slug=post_slug)
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@router.delete('/{post_slug}')
@async_base_crud_route(200)
async def delete_post(uow: UOWDep,
                      post_slug: str,
                      user: User = Depends(current_active_user)):
    await PostsService.delete_post(uow, post_slug, user.id)
    return []
