from contextlib import asynccontextmanager

from fastapi import FastAPI
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
# from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_oauth2_redirect_html, get_swagger_ui_html
# from starlette.staticfiles import StaticFiles

from src.base_schema import BaseResponse
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.auth.router import router as auth_router
from src.profile.router import router as profile_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan,
              validation_error_model=BaseResponse)

# app.mount('/static', StaticFiles(directory='static'), name='static')


# @app.get("/docs", include_in_schema=False)
# async def custom_swagger_ui_html():
#     return get_swagger_ui_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - Swagger UI",
#         oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
#         swagger_js_url="/static/swagger-ui-bundle.js",
#         swagger_css_url="/static/swagger-ui.css",
#     )
#
#
# @app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
# async def swagger_ui_redirect():
#     return get_swagger_ui_oauth2_redirect_html()
#
#
# @app.get("/redoc", include_in_schema=False)
# async def redoc_html():
#     return get_redoc_html(
#         openapi_url=app.openapi_url,
#         title=app.title + " - ReDoc",
#         redoc_js_url="/static/redoc.standalone.js",
#     )


app.include_router(router=auth_router)
app.include_router(router=profile_router)




@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(status_code=422,
                        content=BaseResponse(
                            message="Failed",
                            errors=[str(exc)],
                        ).model_dump())




