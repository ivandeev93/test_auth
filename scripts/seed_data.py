import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from database import async_session_maker
from models.roles import Role
from models.permissions import Permission
from models.role_permissions import RolePermission
from models.users import User
from auth import hash_password

async def seed():
    async with async_session_maker() as db:
        # Роли
        admin_role = Role(name="admin")
        client_role = Role(name="client")
        db.add_all([admin_role, client_role])
        await db.commit()

        # Права
        perms = [
            Permission(resource="items", action="read"),
            Permission(resource="items", action="create"),
            Permission(resource="items", action="update"),
            Permission(resource="items", action="delete")
        ]
        db.add_all(perms)
        await db.commit()

        # Назначение прав роли client
        rp_client = [RolePermission(role_id=client_role.id, permission_id=perms[0].id)]
        db.add_all(rp_client)
        await db.commit()

        # Назначение прав роли admin
        rp_admin = [RolePermission(role_id=admin_role.id, permission_id=p.id) for p in perms]
        db.add_all(rp_admin)
        await db.commit()

        # Пользователи
        admin_user = User(name="Admin User", email="admin@example.com",
                          hashed_password=hash_password("AdminPass123"), role_id=admin_role.id)
        client_user = User(name="Client User", email="client@example.com",
                           hashed_password=hash_password("ClientPass123"), role_id=client_role.id)
        db.add_all([admin_user, client_user])
        await db.commit()

asyncio.run(seed())
