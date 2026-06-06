from fastapi import FastAPI
from app.routers.user_routers import router as user_router


app = FastAPI(
    title="Book Management System"
)

app.include_router(user_router)
