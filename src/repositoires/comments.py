from src.db.models.comments import Comment
from src.repositoires.base_repository import SQLAlchemyRepository


class CommentsRepository(SQLAlchemyRepository):
    model = Comment
    model_name = 'Комментарий'
