from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.crud import TopicCRUD
from app.schemas import Topic, TopicCreate, TopicUpdate, MessageResponse

router = APIRouter()


@router.post("/topics", response_model=Topic, status_code=201)
async def create_topic(
        topic: TopicCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать новую тему"""
    # Проверяем уникальность имени темы
    existing_topic = await TopicCRUD.get_topic_by_name(db, topic.name)
    if existing_topic:
        raise HTTPException(
            status_code=400,
            detail=f"Topic with name '{topic.name}' already exists"
        )

    return await TopicCRUD.create_topic(db, topic)


@router.get("/topics", response_model=List[Topic])
async def get_topics(
        skip: int = Query(0, ge=0, description="Количество пропускаемых элементов"),
        limit: int = Query(100, ge=1, le=100, description="Максимальное количество элементов"),
        db: AsyncSession = Depends(get_db)
):
    """Получить список тем"""
    return await TopicCRUD.get_topics(db, skip, limit)


@router.get("/topics/{topic_id}", response_model=Topic)
async def get_topic(
        topic_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить тему по ID"""
    topic = await TopicCRUD.get_topic(db, topic_id)
    if not topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return topic


@router.put("/topics/{topic_id}", response_model=Topic)
async def update_topic(
        topic_id: int,
        topic_update: TopicUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновить тему"""
    # Если обновляется имя, проверяем уникальность
    if topic_update.name:
        existing_topic = await TopicCRUD.get_topic_by_name(db, topic_update.name)
        if existing_topic and existing_topic.id != topic_id:
            raise HTTPException(
                status_code=400,
                detail=f"Topic with name '{topic_update.name}' already exists"
            )

    updated_topic = await TopicCRUD.update_topic(db, topic_id, topic_update)
    if not updated_topic:
        raise HTTPException(status_code=404, detail="Topic not found")
    return updated_topic


@router.delete("/topics/{topic_id}", response_model=MessageResponse)
async def delete_topic(
        topic_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удалить тему (и все связанные посты)"""
    success = await TopicCRUD.delete_topic(db, topic_id)
    if not success:
        raise HTTPException(status_code=404, detail="Topic not found")
    return MessageResponse(message="Topic deleted successfully")