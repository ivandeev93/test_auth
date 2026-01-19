from fastapi import FastAPI
from routers import users
from routers import admin
from routers import mock_objects


# Создаём приложение FastAPI
app = FastAPI(
    title="Auth & RBAC Service",
    description="Система аутентификации и разграничения прав доступа",
)

# Подключение маршрутов
app.include_router(users.router)
app.include_router(admin.router)
app.include_router(mock_objects.router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать!"}