# Kitsu Backend

Авторитетный API для фронтенда Kitsu. FastAPI предоставляет REST эндпоинты, работает с PostgreSQL через async SQLAlchemy 2.x и миграции Alembic. Исторический PocketBase не используется.

## Назначение и зона ответственности

- Аутентификация/авторизация, выпуск access/refresh токенов.
- Каталог аниме, поиск, коллекции, избранное, просмотры.
- Выдача и сохранение аватаров пользователей по HTTP (`/media/avatars`).

## Технологии

- FastAPI, Uvicorn
- SQLAlchemy 2 (async) + asyncpg
- Alembic
- PyJWT, passlib (bcrypt)

## Переменные окружения (полный список)

Скопируйте `.env.example` в `.env` и задайте значения:

- `SECRET_KEY` — обязательный ключ подписи JWT; без него сервис не стартует.
- `DATABASE_URL` — строка подключения `postgresql+asyncpg://USER:PASS@HOST:PORT/DB`.
  - Для `backend/docker-compose.yml` можно вместо этого задать `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD` — compose соберёт `DATABASE_URL` автоматически.
- `ACCESS_TOKEN_EXPIRE_MINUTES` — время жизни access-токена в минутах (по умолчанию 30).
- `REFRESH_TOKEN_EXPIRE_DAYS` — срок жизни refresh-токена в днях (по умолчанию 14).
- `ALGORITHM` — алгоритм подписи JWT, по умолчанию `HS256`.
- `ALLOWED_ORIGINS` — список для CORS, через запятую. Для продакшна указывайте конкретные домены.
  - При `allow_credentials=true` браузер блокирует `Access-Control-Allow-Origin: *`: со значением `*` куки/авторизационные заголовки не отправляются и ответ считается небезопасным, поэтому указывайте точные origin.
- `DEBUG` — `true`/`false`, включает отладочный вывод и SQL echo.

## Локальный запуск (без Docker)

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -e .
export SECRET_KEY="change-me"
export DATABASE_URL="postgresql+asyncpg://kitsu:kitsu@localhost:5432/kitsu"
uvicorn app.main:app --reload
```

## Alembic: когда и как применять миграции

- Применять при каждом изменении схемы и перед продакшн-деплоем: `alembic upgrade head`.
  - На Render выполняйте команду перед приёмом трафика: либо вручную через Render Shell (одиночный запуск), либо оформив Render Release Command с `alembic upgrade head`, чтобы миграции шли до старта веб-процесса.
- Создавать новые версии при изменении моделей: `alembic revision -m "описание"`.
- В составе Docker-композа миграции можно выполнить через `docker compose -f backend/docker-compose.yml run --rm backend alembic upgrade head`.

## Запуск через Docker (обзор)

- Файл `backend/docker-compose.yml` поднимает PostgreSQL и бэкенд.
- Перед стартом задать переменные (`DATABASE_URL` или `DB_*`, `SECRET_KEY`, CORS и т.д.).
- Запуск: `docker compose -f backend/docker-compose.yml up --build`.
- Swagger доступен на `http://localhost:8000/docs`.

## Загрузки и аватары

- Файлы хранятся в `backend/uploads/avatars` на файловой системе контейнера.
- Раздаются статикой по `GET /media/avatars/<имя-файла>` из FastAPI.
- На Render файловая система эфемерна: без примонтированного тома аватары теряются при перезапусках. Обязательно используйте постоянное хранилище для этого каталога.

## Ограничения текущего MVP

- CRUD пользователей (кроме загрузки аватара) реализован заглушками.
- CORS по умолчанию разрешает `*`; для реальных доменов требуется настройка `ALLOWED_ORIGINS`.
- `/health` не проверяет подключение к БД.
- Один refresh-токен на пользователя; многосессионность не поддерживается.
- Нет rate limiting и защиты от brute force на auth-эндпоинтах.
- Загрузки локальные и без внешнего хранилища; без тома данные теряются при деплое.
