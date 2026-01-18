from pydantic import BaseModel, Field, ConfigDict, EmailStr


class UserCreate(BaseModel):
    """
    Модель для создания пользователя.
    Используется в POST запросах.
    """
    name: str = Field(description="Имя пользователя")
    email: EmailStr = Field(description="Email пользователя")
    password: str = Field(min_length=8, description="Пароль (минимум 8 символов)")
    password_repeat: str = Field(min_length=8, description="Повтор пароля")
    role: str = Field(default="client", pattern="^(client|admin)$", description="Роль: 'client' или 'admin'")


class UserUpdate(BaseModel):
    """
    Модель для обновления пользователя.
    Используется в PUT и PATCH запросах.
    """
    name: str | None = None
    password: str | None = Field(default=None, min_length=8, description="Ввод нового пароля")


class User(BaseModel):
    """
    Модель для ответа с данными пользователя.
    Используется в GET-запросах.
    """
    id: int = Field(description="Уникальный идентификатор пользователя")
    name: str = Field(description="Имя пользователя")
    email: EmailStr = Field(description="Email пользователя")
    is_active: bool = Field(description="Активность пользователя")
    role: str = Field(description="Роль пользователя")

    model_config = ConfigDict(from_attributes=True)
