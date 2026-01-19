# create_tables.py
import asyncio
from database import async_engine, Base
from models import users, roles, permissions, role_permissions  # импорт всех моделей, чтобы SQLAlchemy их увидел

async def init_models():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)  # создаём все таблицы
    print("All tables created successfully!")

asyncio.run(init_models())
