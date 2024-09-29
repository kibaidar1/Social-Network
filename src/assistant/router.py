from fastapi import APIRouter, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from fastapi.exceptions import ValidationException
from fastapi_users.schemas import model_dump
from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.assistant.models import Assistant
from src.assistant.schemas import AssistantRead, AssistantCreate
from src.auth.base_config import current_active_user
from src.auth.models import User
from src.auth.schemas import BaseResponse
from src.database import get_async_session

router = APIRouter(
    prefix="/assistants",
    tags=["assistants"]
)


@router.get('/')
async def get_assistants(session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(current_active_user)):
    # try:
    query = select(Assistant)
    assistants = await session.execute(query)
    return assistants.all()
    # return JSONResponse(status_code=200,
    #                     content=[json.dumps(a) for a in assistants.all()])

    # except Exception as e:
    #     return JSONResponse(status_code=500,
    #                         content=BaseResponse(
    #                             message='Failed',
    #                             errors={'error': 'Unknown error'},
    #                         ).model_dump())


@router.get('/{assistant_id}')
async def get_assistant(assistant_id: int, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)):
    # try:
    query = select(Assistant).where(Assistant.id == assistant_id)
    assistant = await session.execute(query)
    return AssistantRead.model_validate(assistant.scalar_one(), from_attributes=True)

    # except Exception as e:
    #     return JSONResponse(status_code=500,
    #                         content=BaseResponse(
    #                             message='Failed',
    #                             errors={'error': 'Unknown error'},
    #                         ).model_dump())


@router.post('/', response_class=JSONResponse)
async def add_assistant(assistant: AssistantCreate, session: AsyncSession = Depends(get_async_session),
                        user: User = Depends(current_active_user)) -> JSONResponse:
    # try:
    stmt = insert(Assistant).values(**assistant.model_dump())
    await session.execute(stmt)
    await session.commit()
    return JSONResponse(status_code=200,
                        content=BaseResponse(
                            message='Success',
                            data=[assistant],
                        ).model_dump())

    # except ValidationException as e:
    #     return JSONResponse(status_code=400,
    #                         content=BaseResponse(
    #                             message='Failed',
    #                             errors=e.errors(),
    #                         ).model_dump())
    #
    # except Exception as e:
    #     return JSONResponse(status_code=500,
    #                         content=BaseResponse(
    #                             message='Failed',
    #                             errors={'error': str(e)},
    #                         ).model_dump())

