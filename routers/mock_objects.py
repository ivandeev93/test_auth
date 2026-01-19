from fastapi import APIRouter, Depends
from auth import get_current_user, check_permission

router = APIRouter(prefix="/mock", tags=["mock"])

# Пример бизнес-объектов
items = [
    {"id": 1, "name": "Item A"},
    {"id": 2, "name": "Item B"},
    {"id": 3, "name": "Item C"},
]

@router.get("/items")
async def list_items(permission: bool = Depends(check_permission("items", "read"))):
    return items


@router.post("/items")
async def create_item(item: dict, permission: bool = Depends(check_permission("items", "create"))):
    new_id = max(i["id"] for i in items) + 1
    item["id"] = new_id
    items.append(item)
    return item
