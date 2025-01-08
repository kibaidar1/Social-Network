from src.api.routers.auth import router as auth_router
from src.api.routers.users import router as users_router
from src.api.routers.profiles import router as profiles_router
from src.api.routers.comments import router as comments_router
from src.api.routers.posts import router as posts_router


all_routers = [auth_router,
               users_router,
               profiles_router,
               posts_router,
               comments_router
               ]
