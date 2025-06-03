from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import List, Optional


# Схемы для тем
class TopicBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="Название темы")
    description: Optional[str] = Field(None, max_length=500, description="Описание темы")


class TopicCreate(TopicBase):
    pass


class TopicUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)


class Topic(TopicBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime


class TopicWithPosts(Topic):
    posts: List["PostSummary"] = []


# Схемы для комментариев
class CommentBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000, description="Содержание комментария")
    author: str = Field(..., min_length=1, max_length=100, description="Автор комментария")


class CommentCreate(CommentBase):
    pass


class CommentUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    author: Optional[str] = Field(None, min_length=1, max_length=100)


class Comment(CommentBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    post_id: int
    created_at: datetime


# Схемы для постов
class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200, description="Заголовок поста")
    content: str = Field(..., min_length=1, description="Содержание поста")
    topic_id: int = Field(..., gt=0, description="ID темы")


class PostCreate(PostBase):
    pass


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1)
    topic_id: Optional[int] = Field(None, gt=0)


class PostSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    created_at: datetime
    topic_id: int


class Post(PostBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    created_at: datetime
    updated_at: datetime
    topic: Topic
    comments: List[Comment] = []


class PostList(BaseModel):
    items: List[PostSummary]
    total: int
    page: int
    size: int
    pages: int


# Схема ответа с сообщением
class MessageResponse(BaseModel):
    message: str


# Обновляем forward references
TopicWithPosts.model_rebuild()