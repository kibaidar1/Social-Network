from typing import Any

from pydantic import BaseModel


class BaseResponse(BaseModel):
    message: str
    data: list or None = None
    errors: list or None = None
    meta: None or Any = None

