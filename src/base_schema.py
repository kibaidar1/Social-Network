from functools import wraps
from typing import Any

from pydantic import BaseModel
from sqlalchemy.exc import NoResultFound, IntegrityError
from starlette.responses import JSONResponse


class BaseResponse(BaseModel):
    message: str
    data: list or None = None
    errors: list or None = None
    meta: None or Any = None


def async_base_crud_route(success_status: int):
    def decorator(rout):
        @wraps(rout)
        async def wrapper(*args, **kwargs):
            status_code = success_status
            message = 'Success'
            data = []
            errors = []

            try:
                result = await rout(*args, **kwargs)
                if result:
                    if isinstance(result, list):
                        data.extend(result)
                    else:
                        data.append(result)

            except NoResultFound as e:
                print(e)
                message = 'Failed'
                status_code = 404
                errors.append('Instance is not exists')

            except IntegrityError as e:
                print(e)
                message = 'Failed'
                status_code = 400
                errors.append("Instance already exists")

            except Exception as e:
                print(e)
                message = "Failed"
                status_code = 500
                errors.append('Unknown error')

            finally:
                return JSONResponse(status_code=status_code,
                                    content=BaseResponse(
                                        message=message,
                                        data=data,
                                        errors=errors,
                                    ).model_dump())

        return wrapper

    return decorator

