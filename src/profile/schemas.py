from typing import Any

from pydantic import EmailStr, BaseModel, Json, Field, field_validator, ConfigDict

from src.auth.schemas import UserRead

NameField = Field(min_length=1, max_length=255)


class ProfileCreateUpdate(BaseModel):
    name: str = NameField
    surname: str = NameField

    # Валидатор для приведения имени к заглавной букве
    @field_validator("name", "surname")
    def capitalize_name(cls, value):
        return value.capitalize()  # Приведение к заглавной букве


class ProfileRead(BaseModel):
    id: int
    user: UserRead
    name: str = NameField
    surname: str = NameField
    photo_url: str | None = None

    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)




