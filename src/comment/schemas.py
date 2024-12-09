from pydantic import BaseModel, ConfigDict

from src.auth.schemas import UserReadAll


class CommentCreateUpdate(BaseModel):
    text: str


class CommentRead(BaseModel):
    id: int
    text: str
    user: UserReadAll

    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)

