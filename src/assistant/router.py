from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.assistant.models import Assistant
from src.assistant.schemas import AssistantRead, AssistantCreate
from src.auth.base_config import current_active_user
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix="/assistants",
    tags=["assistants"]
)


@router.get('/', response_model=List[AssistantRead])
async def get_assistants(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    query = select(Assistant)
    assistants = await session.execute(query)
    return assistants.all()


@router.get('/{assistant_id}', response_model=AssistantRead)
async def get_assistant(assistant_id: int, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    query = select(Assistant).where(Assistant.id == assistant_id)
    result = await session.execute(query)
    return result.scalar_one()


@router.post('/', response_model=AssistantCreate)
async def add_assistant(assistant: AssistantCreate, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    stmt = insert(Assistant).values(**assistant.model_dump())
    await session.execute(stmt)
    await session.commit()
    return assistant
