import asyncio
from typing import AsyncGenerator

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from starlette.testclient import TestClient

from src.database import Base, get_async_session
from src.main import app

DATABASE_URL = "sqlite+aiosqlite:///test_database.db"

test_engine = create_async_engine(DATABASE_URL)
async_session_maker = sessionmaker(test_engine, class_=AsyncSession, expire_on_commit=False)
Base.metadata.bind = test_engine


async def test_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

app.dependency_overrides[get_async_session] = test_get_async_session


@pytest.fixture(scope='session')
async def prepare_database():
    async with test_engine.begin as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with test_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope='function')
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


client = TestClient(app)


@pytest.fixture(scope='session')
async def async_client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url='http://test') as async_client:
        yield async_client

