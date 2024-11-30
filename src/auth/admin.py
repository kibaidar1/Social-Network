from sqladmin import ModelView

from src.auth.models import User


class UserAdmin(ModelView, model=User):
    column_list = [User.id, User.email, User.username, User.created_at]
    column_sortable_list = [User.id,  User.email, User.username, User.created_at]
    column_default_sort = (User.created_at, True)
    page_size = 50
    page_size_options = [25, 50, 100, 200]
    can_create = False


