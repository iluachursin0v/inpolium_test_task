from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional
import math

from app.database import get_db
from app.crud import PostCRUD, TopicCRUD
from app.schemas import Post, PostCreate, PostUpdate, PostList, PostSummary, MessageResponse

router = APIRouter()


@router.post("/posts", response_model=Post, status_code=201)
async def create_post(
        post: PostCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать новый пост"""
    # Проверяем существование темы
    topic = await TopicCRUD.get_topic(db, post.topic_id)
    if not topic:
        raise HTTPException(
            status_code=404,
            detail=f"Topic with id {post.topic_id} not found"
        )

    return await PostCRUD.create_post(db, post)


@router.get("/posts", response_model=PostList)
async def get_posts(
        page: int = Query(1, ge=1, description="Номер страницы"),
        size: int = Query(10, ge=1, le=100, description="Количество элементов на странице"),
        topic_id: Optional[int] = Query(None, ge=1, description="Фильтр по теме"),
        db: AsyncSession = Depends(get_db)
):
    """Получить список постов с пагинацией"""
    skip = (page - 1) * size

    # Если указан topic_id, проверяем его существование
    if topic_id:
        topic = await TopicCRUD.get_topic(db, topic_id)
        if not topic:
            raise HTTPException(
                status_code=404,
                detail=f"Topic with id {topic_id} not found"
            )

    posts, total = await PostCRUD.get_posts(db, skip=skip, limit=size, topic_id=topic_id)

    # Преобразуем в PostSummary для списка
    post_summaries = [
        PostSummary(
            id=post.id,
            title=post.title,
            created_at=post.created_at,
            topic_id=post.topic_id
        ) for post in posts
    ]

    pages = math.ceil(total / size) if total > 0 else 1

    return PostList(
        items=post_summaries,
        total=total,
        page=page,
        size=size,
        pages=pages
    )


@router.get("/posts/{post_id}", response_model=Post)
async def get_post(
        post_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить пост по ID"""
    post = await PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post


@router.put("/posts/{post_id}", response_model=Post)
async def update_post(
        post_id: int,
        post_update: PostUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновить пост"""
    # Если обновляется topic_id, проверяем его существование
    if post_update.topic_id:
        topic = await TopicCRUD.get_topic(db, post_update.topic_id)
        if not topic:
            raise HTTPException(
                status_code=404,
                detail=f"Topic with id {post_update.topic_id} not found"
            )

    updated_post = await PostCRUD.update_post(db, post_id, post_update)
    if not updated_post:
        raise HTTPException(status_code=404, detail="Post not found")
    return updated_post


@router.delete("/posts/{post_id}", response_model=MessageResponse)
async def delete_post(
        post_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удалить пост (и все его комментарии)"""
    success = await PostCRUD.delete_post(db, post_id)
    if not success:
        raise HTTPException(status_code=404, detail="Post not found")
    return MessageResponse(message="Post deleted successfully")