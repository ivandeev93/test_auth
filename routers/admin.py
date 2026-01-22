from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.roles import Role
from models.permissions import Permission
from models.role_permissions import RolePermission
from schemas.users import User as UserSchema
from db_depends import get_async_db
from auth import get_current_admin
from sqlalchemy.exc import IntegrityError, SQLAlchemyError


router = APIRouter(prefix="/admin", tags=["admin"])


@router.get("/roles")
async def list_roles(db: AsyncSession = Depends(get_async_db),
                     admin: UserSchema = Depends(get_current_admin)):
    """
    Возвращает список ролей
    """
    result = await db.scalars(select(Role))
    return result.all()


@router.post("/roles")
async def create_role(name: str, db: AsyncSession = Depends(get_async_db),
                      admin: UserSchema = Depends(get_current_admin)):
    """
    Создание ролей с проверкой уникальности.
    """
    existing = await db.scalars(select(Role).where(Role.name == name))
    if existing.first():
        raise HTTPException(status_code=400, detail="Role already exists")
    role = Role(name=name)
    db.add(role)
    await db.commit()
    await db.refresh(role)
    return role


@router.get("/permissions")
async def list_permissions(db: AsyncSession = Depends(get_async_db),
                           admin: UserSchema = Depends(get_current_admin)):
    """
    Возвращает список прав.
    """
    result = await db.scalars(select(Permission))
    return result.all()


@router.post("/permissions")
async def create_permission(resource: str, action: str,
                            db: AsyncSession = Depends(get_async_db),
                            admin: UserSchema = Depends(get_current_admin)):
    """
    Создание прав с проверкой уникальности.
    """
    existing = await db.scalars(
        select(Permission).where(Permission.resource == resource, Permission.action == action)
    )
    if existing.first():
        raise HTTPException(status_code=400, detail="Permission already exists")
    perm = Permission(resource=resource, action=action)
    db.add(perm)
    await db.commit()
    await db.refresh(perm)
    return perm


@router.post("/roles/{role_id}/permissions/{permission_id}")
async def assign_permission_to_role(role_id: int, permission_id: int,
                                    db: AsyncSession = Depends(get_async_db),
                                    admin: UserSchema = Depends(get_current_admin)):
    """
    Добавление прав ролям
    """
    rp = RolePermission(role_id=role_id, permission_id=permission_id)
    db.add(rp)
    try:
        await db.commit()
    except IntegrityError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Permission already assigned"
        )
    except SQLAlchemyError:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Database error"
        )

    return {"detail": "Permission assigned"}