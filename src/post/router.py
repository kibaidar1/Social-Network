import re

from fastapi import Depends
from fastapi.routing import APIRouter
from slugify import slugify
from sqlalchemy import select, insert, update, delete
from sqlalchemy.exc import NoResultFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status
from starlette.responses import RedirectResponse

from src.auth.base_config import current_active_user
from src.auth.models import User
from src.base_schema import async_base_crud_route
from src.database import get_async_session
from src.post.models import Post
from src.post.schemas import PostRead, PostCreate, PostReadDetail, PostUpdate

router = APIRouter(prefix='/posts',
                   tags=['posts'])


async def generate_unique_slug(session: AsyncSession, title: str) -> str:
    # Генерация начального slug на основе заголовка
    base_slug = slugify(title)

    # Проверяем, существует ли уже точный slug без числового суффикса
    stmt_exact = select(Post).filter(Post.slug == base_slug)
    result_exact = await session.execute(stmt_exact)
    existing_post = result_exact.scalars().first()

    # Если точный slug существует, увеличиваем суффикс
    if existing_post:
        # Собираем все числовые суффиксы из базы данных для данного base_slug
        stmt = select(Post).filter(Post.slug.like(f"{base_slug}-%"))
        result = await session.execute(stmt)
        posts = result.scalars().all()

        # Собираем все числовые суффиксы
        suffixes = set()
        for post in posts:
            match = re.match(r"^" + re.escape(base_slug) + r"-(\d+)$", post.slug)
            if match:
                suffix = int(match.group(1))  # Извлекаем числовой суффикс
                suffixes.add(suffix)

        # Находим первый пропущенный суффикс
        next_suffix = 1
        while next_suffix in suffixes:
            next_suffix += 1

        # Создаем новый slug с найденным суффиксом
        unique_slug = f"{base_slug}-{next_suffix}"
    else:
        # Если точный slug без суффикса не существует, то он уникален
        unique_slug = base_slug

    return unique_slug


@router.get('/')
@async_base_crud_route(200)
async def get_all_posts(session: AsyncSession = Depends(get_async_session)):
    stmt = select(Post)
    res = await session.execute(stmt)
    posts = res.scalars().all()
    return [PostRead.model_validate(p, from_attributes=True) for p in posts]


@router.get('/{post_slug}')
@async_base_crud_route(200)
async def get_post_detail(post_slug: str,
                          session: AsyncSession = Depends(get_async_session)):
    stmt = select(Post).where(Post.slug == post_slug)
    res = await session.execute(stmt)
    post = res.scalar_one()
    print(post.user_id)
    return PostReadDetail.model_validate(post, from_attributes=True)


@router.get('/my_posts')
@async_base_crud_route(200)
async def get_my_posts(session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(current_active_user)):
    stmt = select(Post).where(Post.user_id == user.id)
    res = await session.execute(stmt)
    posts = res.scalars().all()
    return [PostRead.model_validate(p, from_attributes=True) for p in posts]


@router.post('/')
async def create_post(post_data: PostCreate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    stmt = (insert(Post)
            .values(**post_data.model_dump(),
                    user_id=user.id,
                    slug=await generate_unique_slug(session, post_data.title))
            .returning(Post.slug))
    res = await session.execute(stmt)
    post_slug = res.scalar_one()
    url = f'{router.prefix}/{post_slug}'
    await session.commit()
    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@router.put('/{post_slug}')
async def update_post(post_slug: str,
                      post_data: PostUpdate,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    data = post_data.model_dump(exclude_unset=True)
    print(data)
    if post_data.title:
        data['slug'] = await generate_unique_slug(session, post_data.title)
    stmt = (update(Post)
            .where(Post.slug == post_slug and Post.user_id == user.id)
            .values(**data)
            .returning(Post.slug))

    res = await session.execute(stmt)
    post_slug = res.scalar_one()
    url = f'{router.prefix}/{post_slug}'
    if not res:
        raise NoResultFound
    await session.commit()

    return RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)


@router.delete('/{post_slug}')
@async_base_crud_route(200)
async def delete_post(post_slug: str,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(current_active_user)):
    stmt = (delete(Post)
            .where(Post.slug == post_slug and Post.user_id == user.id))
    res = await session.execute(stmt)
    if not res.rowcount:
        raise NoResultFound
    await session.commit()
