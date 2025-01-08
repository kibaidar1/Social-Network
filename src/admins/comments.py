from sqladmin import ModelView

from src.db.models.comments import Comment


class CommentAdmin(ModelView, model=Comment):
    column_list = [Comment.user, Comment.post, Comment.created_at, Comment.updated_at]
    icon = 'fa fa-'
    column_sortable_list = column_list
    column_default_sort = (Comment.created_at, True)
    page_size = 50
    page_size_options = [25, 50, 100, 200]