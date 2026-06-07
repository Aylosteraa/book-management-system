from fastapi import FastAPI
from app.routers.user_routers import router as user_router
from app.routers.book_routers import router as book_router
from app.routers.health_router import router as health_router

app = FastAPI(
    title="Book Management System"
)

app.include_router(user_router)
app.include_router(book_router)
app.include_router(health_router)
