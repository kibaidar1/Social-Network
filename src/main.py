from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin
from starlette.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles

from src.admins.comments import CommentAdmin
from src.admins.posts import PostAdmin
from src.admins.profiles import ProfileAdmin
from src.admins.users import UserAdmin
from src.api.base_route_schema import BaseResponse
from src.api.exception_handlers import init_exception_handlers
from src.api.routers.routers import all_routers
# from fastapi_cache import FastAPICache
# from fastapi_cache.backends.redis import RedisBackend
# from redis import asyncio as aioredis
# from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_oauth2_redirect_html, get_swagger_ui_html
# from starlette.staticfiles import StaticFiles

from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from src.database import engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    yield


app = FastAPI(lifespan=lifespan,
              validation_error_model=BaseResponse)

admin = Admin(app, engine)

admin.add_view(UserAdmin)
admin.add_view(ProfileAdmin)
admin.add_view(PostAdmin)
admin.add_view(CommentAdmin)

origins = ['http://localhost:5174', 'http://http://127.0.0.1:5174']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount('/photos', StaticFiles(directory='static/photos'), name='photos')



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

for router in all_routers:
    app.include_router(router)


init_exception_handlers(app)




