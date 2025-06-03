from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.database import get_db
from app.crud import CommentCRUD, PostCRUD
from app.schemas import Comment, CommentCreate, CommentUpdate, MessageResponse

router = APIRouter()


@router.post("/posts/{post_id}/comments", response_model=Comment, status_code=201)
async def create_comment(
        post_id: int,
        comment: CommentCreate,
        db: AsyncSession = Depends(get_db)
):
    """Создать комментарий к посту"""
    # Проверяем существование поста
    post = await PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return await CommentCRUD.create_comment(db, comment, post_id)


@router.get("/posts/{post_id}/comments", response_model=List[Comment])
async def get_comments_by_post(
        post_id: int,
        skip: int = Query(0, ge=0, description="Количество пропускаемых элементов"),
        limit: int = Query(100, ge=1, le=100, description="Максимальное количество элементов"),
        db: AsyncSession = Depends(get_db)
):
    """Получить комментарии к посту"""
    # Проверяем существование поста
    post = await PostCRUD.get_post(db, post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")

    return await CommentCRUD.get_comments_by_post(db, post_id, skip, limit)


@router.get("/comments/{comment_id}", response_model=Comment)
async def get_comment(
        comment_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Получить комментарий по ID"""
    comment = await CommentCRUD.get_comment(db, comment_id)
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment


@router.put("/comments/{comment_id}", response_model=Comment)
async def update_comment(
        comment_id: int,
        comment_update: CommentUpdate,
        db: AsyncSession = Depends(get_db)
):
    """Обновить комментарий"""
    updated_comment = await CommentCRUD.update_comment(db, comment_id, comment_update)
    if not updated_comment:
        raise HTTPException(status_code=404, detail="Comment not found")
    return updated_comment


@router.delete("/comments/{comment_id}", response_model=MessageResponse)
async def delete_comment(
        comment_id: int,
        db: AsyncSession = Depends(get_db)
):
    """Удалить комментарий"""
    success = await CommentCRUD.delete_comment(db, comment_id)
    if not success:
        raise HTTPException(status_code=404, detail="Comment not found")
    return MessageResponse(message="Comment deleted successfully")