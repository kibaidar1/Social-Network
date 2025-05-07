from functools import wraps
from typing import Any

from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, IntegrityError
from starlette.responses import JSONResponse


class BaseResponse(BaseModel):
    message: str = 'ОК'
    data:  list[dict] | dict | None = None


