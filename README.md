Blog API
Асинхронный REST API сервис для управления блогом, построенный на FastAPI.
Возможности

📝 Посты: Создание, просмотр, обновление и удаление постов
💬 Комментарии: Добавление и управление комментариями к постам
🏷️ Темы: Организация постов по темам
🔍 Фильтрация: Поиск постов по темам
📄 Пагинация: Постраничная навигация
⚡ Асинхронность: Все операции с базой данных асинхронные

Технологии

FastAPI - современный веб-фреймворк для Python
SQLAlchemy - асинхронная ORM
SQLite - база данных (с возможностью переключения на PostgreSQL)
Pydantic - валидация данных
Uvicorn - ASGI сервер

Структура проекта
blog-api/
├── app/
│   ├── __init__.py
│   ├── models.py          # Модели базы данных
│   ├── schemas.py         # Pydantic схемы валидации
│   ├── database.py        # Конфигурация базы данных
│   ├── crud.py           # CRUD операции
│   └── routers/
│       ├── __init__.py
│       ├── posts.py      # Эндпоинты для постов
│       ├── comments.py   # Эндпоинты для комментариев
│       └── topics.py     # Эндпоинты для тем
├── main.py               # Главный файл приложения
├── requirements.txt      # Зависимости
└── README.md            # Документация

Установка и запуск
1. Клонирование и настройка
bash# Создание виртуального окружения
python -m venv venv

# Активация окружения
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установка зависимостей
pip install -r requirements.txt
2. Запуск приложения
bash# Запуск в режиме разработки
python main.py

# Или через uvicorn
uvicorn main:app --reload
Приложение будет доступно по адресу: http://localhost:8000
3. Документация API
После запуска сервера документация будет доступна по адресам:

Swagger UI: http://localhost:8000/docs
ReDoc: http://localhost:8000/redoc

API Endpoints
Темы (Topics)
МетодЭндпоинтОписаниеPOST/api/topicsСоздать темуGET/api/topicsПолучить список темGET/api/topics/{id}Получить тему по IDPUT/api/topics/{id}Обновить темуDELETE/api/topics/{id}Удалить тему
Посты (Posts)
МетодЭндпоинтОписаниеPOST/api/postsСоздать постGET/api/postsПолучить список постов (с пагинацией и фильтрацией)GET/api/posts/{id}Получить пост по IDPUT/api/posts/{id}Обновить постDELETE/api/posts/{id}Удалить пост
Комментарии (Comments)
МетодЭндпоинтОписаниеPOST/api/posts/{post_id}/commentsСоздать комментарий к постуGET/api/posts/{post_id}/commentsПолучить комментарии постаGET/api/comments/{id}Получить комментарий по IDPUT/api/comments/{id}Обновить комментарийDELETE/api/comments/{id}Удалить комментарий
Примеры использования
Создание темы
bashcurl -X POST "http://localhost:8000/api/topics" \
     -H "Content-Type: application/json" \
     -d '{
       "name": "Технологии",
       "description": "Статьи о современных технологиях"
     }'
Создание поста
bashcurl -X POST "http://localhost:8000/api/posts" \
     -H "Content-Type: application/json" \
     -d '{
       "title": "Введение в FastAPI",
       "content": "FastAPI - это современный веб-фреймворк...",
       "topic_id": 1
     }'
Получение постов с фильтрацией
bash# Все посты (первая страница, 10 элементов)
curl "http://localhost:8000/api/posts?page=1&size=10"

# Посты определённой темы
curl "http://localhost:8000/api/posts?topic_id=1&page=1&size=5"
Добавление комментария
bashcurl -X POST "http://localhost:8000/api/posts/1/comments" \
     -H "Content-Type: application/json" \
     -d '{
       "content": "Отличная статья!",
       "author": "John Doe"
     }'
Модели данных
Topic (Тема)

id: ID темы
name: Название темы (уникальное)
description: Описание темы
created_at: Дата создания

Post (Пост)

id: ID поста
title: Заголовок поста
content: Содержание поста
topic_id: ID темы
created_at: Дата создания
updated_at: Дата обновления

Comment (Комментарий)

id: ID комментария
content: Содержание комментария
author: Автор комментария
post_id: ID поста
created_at: Дата создания

Переменные окружения
Для настройки базы данных можно использовать переменную окружения:
bash# SQLite (по умолчанию)
DATABASE_URL=sqlite+aiosqlite:///./blog.db

# PostgreSQL
DATABASE_URL=postgresql+asyncpg://user:password@localhost/blog_db
Дополнительные возможности

Валидация данных: Все входящие данные валидируются с помощью Pydantic
Обработка ошибок: Корректная обработка всех типов ошибок
CORS: Настроена поддержка CORS для фронтенд приложений
Каскадное удаление: При удалении поста удаляются все его комментарии
Сортировка: Посты сортируются по дате создания (новые первыми)

Тестирование
После запуска сервера вы можете протестировать API используя:

Swagger UI по адресу http://localhost:8000/docs
Любой HTTP клиент (curl, Postman, etc.)
Встроенную интерактивную документацию

Разработка
Для разработки рекомендуется:

Использовать режим reload: uvicorn main:app --reload
Включить логирование SQL запросов (уже настроено в database.py)
Использовать отладчик Python для пошагового выполнения

Лицензия
MIT License