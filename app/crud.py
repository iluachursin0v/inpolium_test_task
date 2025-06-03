from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload
from sqlalchemy import func, desc
from typing import Optional, List
from datetime import datetime

from app.models import Post, Comment, Topic
from app.schemas import PostCreate, PostUpdate, CommentCreate, CommentUpdate, TopicCreate, TopicUpdate


class TopicCRUD:
    @staticmethod
    async def get_topic(db: AsyncSession, topic_id: int) -> Optional[Topic]:
        """Получить тему по ID"""
        result = await db.execute(select(Topic).where(Topic.id == topic_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_topics(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Topic]:
        """Получить список тем"""
        result = await db.execute(
            select(Topic).offset(skip).limit(limit).order_by(Topic.name)
        )
        return result.scalars().all()

    @staticmethod
    async def get_topic_by_name(db: AsyncSession, name: str) -> Optional[Topic]:
        """Получить тему по имени"""
        result = await db.execute(select(Topic).where(Topic.name == name))
        return result.scalar_one_or_none()

    @staticmethod
    async def create_topic(db: AsyncSession, topic: TopicCreate) -> Topic:
        """Создать новую тему"""
        db_topic = Topic(**topic.model_dump())
        db.add(db_topic)
        await db.commit()
        await db.refresh(db_topic)
        return db_topic

    @staticmethod
    async def update_topic(db: AsyncSession, topic_id: int, topic: TopicUpdate) -> Optional[Topic]:
        """Обновить тему"""
        db_topic = await TopicCRUD.get_topic(db, topic_id)
        if db_topic is None:
            return None

        update_data = topic.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_topic, field, value)

        await db.commit()
        await db.refresh(db_topic)
        return db_topic

    @staticmethod
    async def delete_topic(db: AsyncSession, topic_id: int) -> bool:
        """Удалить тему"""
        db_topic = await TopicCRUD.get_topic(db, topic_id)
        if db_topic is None:
            return False

        await db.delete(db_topic)
        await db.commit()
        return True


class PostCRUD:
    @staticmethod
    async def get_post(db: AsyncSession, post_id: int) -> Optional[Post]:
        """Получить пост по ID с темой и комментариями"""
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.topic), selectinload(Post.comments))
            .where(Post.id == post_id)
        )
        return result.scalar_one_or_none()

    @staticmethod
    async def get_posts(
            db: AsyncSession,
            skip: int = 0,
            limit: int = 100,
            topic_id: Optional[int] = None
    ) -> tuple[List[Post], int]:
        """Получить список постов с пагинацией"""
        query = select(Post).options(selectinload(Post.topic))

        if topic_id:
            query = query.where(Post.topic_id == topic_id)

        # Подсчёт общего количества
        count_query = select(func.count(Post.id))
        if topic_id:
            count_query = count_query.where(Post.topic_id == topic_id)

        total_result = await db.execute(count_query)
        total = total_result.scalar()

        # Получение постов с сортировкой по дате создания (новые первыми)
        result = await db.execute(
            query.order_by(desc(Post.created_at)).offset(skip).limit(limit)
        )
        posts = result.scalars().all()

        return posts, total

    @staticmethod
    async def create_post(db: AsyncSession, post: PostCreate) -> Post:
        """Создать новый пост"""
        db_post = Post(**post.model_dump())
        db.add(db_post)
        await db.commit()
        await db.refresh(db_post)

        # Загружаем связанную тему
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.topic), selectinload(Post.comments))
            .where(Post.id == db_post.id)
        )
        return result.scalar_one()

    @staticmethod
    async def update_post(db: AsyncSession, post_id: int, post: PostUpdate) -> Optional[Post]:
        """Обновить пост"""
        db_post = await PostCRUD.get_post(db, post_id)
        if db_post is None:
            return None

        update_data = post.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_post, field, value)

        db_post.updated_at = datetime.utcnow()
        await db.commit()
        await db.refresh(db_post)

        # Перезагружаем с связями
        result = await db.execute(
            select(Post)
            .options(selectinload(Post.topic), selectinload(Post.comments))
            .where(Post.id == db_post.id)
        )
        return result.scalar_one()

    @staticmethod
    async def delete_post(db: AsyncSession, post_id: int) -> bool:
        """Удалить пост"""
        db_post = await PostCRUD.get_post(db, post_id)
        if db_post is None:
            return False

        await db.delete(db_post)
        await db.commit()
        return True


class CommentCRUD:
    @staticmethod
    async def get_comment(db: AsyncSession, comment_id: int) -> Optional[Comment]:
        """Получить комментарий по ID"""
        result = await db.execute(select(Comment).where(Comment.id == comment_id))
        return result.scalar_one_or_none()

    @staticmethod
    async def get_comments_by_post(
            db: AsyncSession,
            post_id: int,
            skip: int = 0,
            limit: int = 100
    ) -> List[Comment]:
        """Получить комментарии к посту"""
        result = await db.execute(
            select(Comment)
            .where(Comment.post_id == post_id)
            .order_by(Comment.created_at)
            .offset(skip)
            .limit(limit)
        )
        return result.scalars().all()

    @staticmethod
    async def create_comment(db: AsyncSession, comment: CommentCreate, post_id: int) -> Comment:
        """Создать новый комментарий"""
        db_comment = Comment(**comment.model_dump(), post_id=post_id)
        db.add(db_comment)
        await db.commit()
        await db.refresh(db_comment)
        return db_comment

    @staticmethod
    async def update_comment(db: AsyncSession, comment_id: int, comment: CommentUpdate) -> Optional[Comment]:
        """Обновить комментарий"""
        db_comment = await CommentCRUD.get_comment(db, comment_id)
        if db_comment is None:
            return None

        update_data = comment.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_comment, field, value)

        await db.commit()
        await db.refresh(db_comment)
        return db_comment

    @staticmethod
    async def delete_comment(db: AsyncSession, comment_id: int) -> bool:
        """Удалить комментарий"""
        db_comment = await CommentCRUD.get_comment(db, comment_id)
        if db_comment is None:
            return False

        await db.delete(db_comment)
        await db.commit()
        return True