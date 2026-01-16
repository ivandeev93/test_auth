from fastapi import FastAPI
from routers import users


# Создаём приложение FastAPI
app = FastAPI(
    title="Сервис пользователей",
)

# Подключение маршрутов
app.include_router(users.router)


# Корневой эндпоинт для проверки
@app.get("/")
async def root():
    """
    Корневой маршрут, подтверждающий, что API работает.
    """
    return {"message": "Добро пожаловать!"}