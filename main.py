from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.database import create_tables
from app.routers import posts, comments, topics


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Создание таблиц при запуске
    await create_tables()
    yield


app = FastAPI(
    title="Blog API",
    description="Асинхронный REST API сервис для управления блогом",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение роутеров
app.include_router(posts.router, prefix="/api", tags=["Posts"])
app.include_router(comments.router, prefix="/api", tags=["Comments"])
app.include_router(topics.router, prefix="/api", tags=["Topics"])


@app.get("/")
async def root():
    return {"message": "Blog API is running"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)