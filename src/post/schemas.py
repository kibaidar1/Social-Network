from pydantic import BaseModel, ConfigDict

from src.auth.schemas import UserReadAll
from src.comment.schemas import CommentRead


class PostCreate(BaseModel):
    title: str
    text: str


class PostUpdate(BaseModel):
    title: str | None = None
    text: str | None = None


class PostRead(BaseModel):
    title: str
    slug: str
    user: UserReadAll

    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)


class PostReadDetail(BaseModel):
    title: str
    slug: str
    text: str
    user: UserReadAll
    comments: list[CommentRead] | None = None

    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)

