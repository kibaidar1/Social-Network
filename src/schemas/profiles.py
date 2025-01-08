from pydantic import BaseModel, Field, field_validator, ConfigDict

NameField = Field(default=None, min_length=1, max_length=255)


class Profile(BaseModel):
    name: str | None = NameField
    surname: str | None = NameField
    photo_url: str | None = ''

    # Валидатор для приведения имени к заглавной букве
    @field_validator("name", "surname")
    def capitalize_name(cls, value):
        if value:
            return value.capitalize()  # Приведение к заглавной букве

    model_config = ConfigDict(from_attributes=True,
                              arbitrary_types_allowed=True)




