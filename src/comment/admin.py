from sqladmin import ModelView

from src.comment.models import Comment
from src.post.models import Post


class CommentAdmin(ModelView, model=Post):
    column_list = [Comment.user, Comment.post, Comment.created_at, Comment.updated_at]
    icon = 'fa fa-'
    column_sortable_list = column_list
    column_default_sort = (Post.created_at, True)
    page_size = 50
    page_size_options = [25, 50, 100, 200]