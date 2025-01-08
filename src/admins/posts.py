from sqladmin import ModelView

from src.db.models.posts import Post


class PostAdmin(ModelView, model=Post):
    column_list = [Post.title, Post.slug, Post.created_at, Post.updated_at]
    icon = 'fa fa-'
    column_sortable_list = [Post.title, Post.slug, Post.user, Post.created_at, Post.updated_at]
    column_default_sort = (Post.created_at, True)
    page_size = 50
    page_size_options = [25, 50, 100, 200]