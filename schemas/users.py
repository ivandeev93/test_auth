from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Модель для создания и обновления пользователя.
    Используется в POST и PUT запросах.
    """
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")
    role: str = Field(default="buyer", pattern="^(client|admin)$", description="Роль: 'client' или 'admin'")


class User(BaseModel):
    """
    Модель для ответа с данными пользователя.
    Используется в GET-запросах.
    """
    id: int = Field(description="Уникальный идентификатор пользователя")
    email: EmailStr = Field(description="Email пользователя")
    is_active: bool = Field(description="Активность пользователя")
    role: str = Field(description="Роль пользователя")

    model_config = ConfigDict(from_attributes=True)
