#!/usr/bin/env python3
"""
Скрипт для тестирования Blog API
Демонстрирует основные возможности API
"""

import asyncio
import aiohttp
import json
from typing import Dict, Any


class BlogAPITester:
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        self.base_url = base_url
        self.session = None

    async def __aenter__(self):
        self.session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()

    async def make_request(self, method: str, endpoint: str, data: Dict[Any, Any] = None) -> Dict[Any, Any]:
        """Выполнить HTTP запрос"""
        url = f"{self.base_url}{endpoint}"

        try:
            if method.upper() == "GET":
                async with self.session.get(url) as response:
                    result = await response.json()
            elif method.upper() == "POST":
                async with self.session.post(url, json=data) as response:
                    result = await response.json()
            elif method.upper() == "PUT":
                async with self.session.put(url, json=data) as response:
                    result = await response.json()
            elif method.upper() == "DELETE":
                async with self.session.delete(url) as response:
                    result = await response.json()

            print(f"{method.upper()} {url}")
            print(f"Status: {response.status}")
            print(f"Response: {json.dumps(result, indent=2, ensure_ascii=False)}")
            print("-" * 50)

            return result

        except Exception as e:
            print(f"Error: {e}")
            return {}

    async def test_full_workflow(self):
        """Тестирует полный рабочий процесс API"""
        print("🚀 Начинаем тестирование Blog API")
        print("=" * 50)

        # 1. Создание тем
        print("📂 Создаём темы...")
        tech_topic = await self.make_request("POST", "/topics", {
            "name": "Технологии",
            "description": "Статьи о современных технологиях и разработке"
        })

        lifestyle_topic = await self.make_request("POST", "/topics", {
            "name": "Образ жизни",
            "description": "Статьи о здоровье, путешествиях и хобби"
        })

        # 2. Получение списка тем
        print("📋 Получаем список тем...")
        await self.make_request("GET", "/topics")

        # 3. Создание постов
        print("📝 Создаём посты...")
        if tech_topic.get("id"):
            post1 = await self.make_request("POST", "/posts", {
                "title": "Введение в FastAPI",
                "content": "FastAPI - это современный, быстрый веб-фреймворк для создания API с Python 3.7+, основанный на стандартных аннотациях типов Python.",
                "topic_id": tech_topic["id"]
            })

            post2 = await self.make_request("POST", "/posts", {
                "title": "Асинхронное программирование в Python",
                "content": "Asyncio позволяет писать конкурентный код с помощью синтаксиса async/await.",
                "topic_id": tech_topic["id"]
            })

        if lifestyle_topic.get("id"):
            post3 = await self.make_request("POST", "/posts", {
                "title": "Продуктивность в удалённой работе",
                "content": "Советы по организации рабочего места и планированию времени при работе из дома.",
                "topic_id": lifestyle_topic["id"]
            })

        # 4. Получение списка постов
        print("📄 Получаем список постов...")
        await self.make_request("GET", "/posts?page=1&size=10")

        # 5. Фильтрация постов по теме
        if tech_topic.get("id"):
            print("🔍 Фильтруем посты по теме 'Технологии'...")
            await self.make_request("GET", f"/posts?topic_id={tech_topic['id']}")

        # 6. Получение конкретного поста
        if post1.get("id"):
            print("📖 Получаем конкретный пост...")
            await self.make_request("GET", f"/posts/{post1['id']}")

        # 7. Добавление комментариев
        print("💬 Добавляем комментарии...")
        if post1.get("id"):
            comment1 = await self.make_request("POST", f"/posts/{post1['id']}/comments", {
                "content": "Отличная статья! Очень помогла разобраться с FastAPI.",
                "author": "Алексей Петров"
            })

            await self.make_request("POST", f"/posts/{post1['id']}/comments", {
                "content": "Спасибо за подробные объяснения. Жду продолжения!",
                "author": "Мария Иванова"
            })

        # 8. Получение комментариев к посту
        if post1.get("id"):
            print("📝 Получаем комментарии к посту...")
            await self.make_request("GET", f"/posts/{post1['id']}/comments")

        # 9. Обновление поста
        if post1.get("id"):
            print("✏️ Обновляем пост...")
            await self.make_request("PUT", f"/posts/{post1['id']}", {
                "title": "Полное введение в FastAPI",
                "content": "FastAPI - это современный, быстрый веб-фреймворк для создания API с Python 3.7+. В этой статье мы подробно рассмотрим все основные возможности фреймворка."
            })

        # 10. Обновление комментария
        if comment1.get("id"):
            print("✏️ Обновляем комментарий...")
            await self.make_request("PUT", f"/comments/{comment1['id']}", {
                "content": "Превосходная статья! Очень помогла разобраться с FastAPI. Рекомендую всем начинающим разработчикам!",
                "author": "Алексей Петров"
            })

        print("✅ Тестирование завершено успешно!")


async def main():
    """Основная функция для запуска тестов"""
    async with BlogAPITester() as tester:
        await tester.test_full_workflow()


if __name__ == "__main__":
    print("Blog API Tester")
    print("Убедитесь, что сервер запущен на http://localhost:8000")
    print()

    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n❌ Тестирование прервано пользователем")
    except Exception as e:
        print(f"❌ Ошибка: {e}")