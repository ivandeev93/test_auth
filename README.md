# Backend-приложение: Система аутентификации и авторизации с RBAC

## Описание проекта

Это backend-приложение реализует **собственную систему аутентификации и авторизации**, включая **ролевое разграничение прав доступа (RBAC)**.  
Приложение не использует готовые механизмы фреймворка “из коробки” для ролей и permissions — всё реализовано вручную.

Основная цель: **предоставить пользователям доступ к ресурсам согласно их роли**, с гибкой системой прав и проверкой доступа через API.

---

## Стек технологий

- Python 3.11+
- FastAPI
- SQLAlchemy (async ORM)
- PostgreSQL
- JWT (JSON Web Token) для аутентификации
- Pydantic для валидации данных

---

## Схема управления доступом (RBAC)

Система доступа в приложении реализована по принципу **RBAC (Role-Based Access Control)** — доступ пользователя определяется его ролью.

### Логика работы

1. **Пользователь** имеет одну **роль** (`role_id`).
2. **Роль** объединяет набор **прав (permissions)**.
3. **Permission** описывает разрешённое действие (`action`) над конкретным ресурсом (`resource`).


### Структура таблиц и связи

- **users**  
  - `id`, `name`, `email`, `hashed_password`, `is_active`, `role_id`  
  - Связь: `role_id` → `roles.id`

- **roles**  
  - `id`, `name` (например: admin, client)  
  - Связь: `Role.role_permissions` — список разрешений роли

- **permissions**  
  - `id`, `resource`, `action`  
  - Определяет ресурс и допустимое действие (например `products:read`, `users:delete`)

- **role_permissions** (вспомогательная таблица)  
  - `role_id` → `roles.id`  
  - `permission_id` → `permissions.id`  
  - Обеспечивает связь «роль ↔ права»  
  - Ограничение `UniqueConstraint(role_id, permission_id)` гарантирует уникальные пары

### Примеры ролей и прав

| Роль   | Ресурс   | Действие |
|--------|----------|----------|
| admin  | products | read     |
| admin  | products | write    |
| admin  | users    | delete   |
| client | products | read     |

### Проверка доступа

- При обращении к ресурсу система вызывает `check_permission(resource, action)`  
- Если пользователь **не залогинен** → 401 Unauthorized  
- Если пользователь **не имеет права** → 403 Forbidden  
- Если пользователь **имеет право** → возвращается запрошенный ресурс

---

## Функционал приложения

### 1. Взаимодействие с пользователем

- **Регистрация** (`POST /users/`)  
  Ввод: `name`, `email`, `password`, `password_repeat`, `role_id`  
  - Проверка совпадения паролей  
  - Проверка уникальности email  
  - Проверка существования роли  

- **Login** (`POST /users/token`)  
  Ввод: `email`, `password`  
  Возвращает `access_token` и `refresh_token` (JWT)  

- **Refresh token** (`POST /users/refresh-token`)  
  Позволяет обновить access_token с помощью refresh_token  

- **Обновление профиля** (`PUT /users/me`)  
  Изменение имени и/или пароля  

- **Удаление пользователя (soft delete)** (`DELETE /users/me`)  
  Меняет `is_active = False`, пользователь больше не может входить  

- **Logout** (`POST /users/logout`)  
  Фиктивный endpoint (клиент удаляет токен)  

---

### 2. Минимальные бизнес-объекты (Mock Views)

- `/products/` — список товаров  
- `/orders/` — список заказов  

Mock Views возвращают либо список объектов, либо ошибки `401`/`403` в зависимости от прав пользователя.

---

### 3. Управление правами (для администратора)

- API для получения и изменения правил реализован через модели `Role`, `Permission`, `RolePermission`  
- Администратор может:  
  - Назначать права ролям  
  - Изменять существующие права  
  - Удалять права  

---

## Запуск проекта

1. Установить зависимости:

```bash
pip install -r requirements.txt

2. Настроить .env:

SECRET_KEY=ваш_секретный_ключ
DATABASE_URL=postgresql+asyncpg://user:password@localhost:5432/dbname


3. Создать таблицы в PostgreSQL через Alembic или SQLAlchemy (create_tabels.py)

### Запуск через Docker

```bash
docker-compose up --build

API будет доступно по адресу:

http://localhost:8000

Swagger-документация:

http://localhost:8000/docs