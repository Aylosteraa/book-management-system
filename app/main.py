from fastapi import FastAPI, Request

from app.routers.user_routers import router as user_router
from app.routers.book_routers import router as book_router
from app.routers.health_router import router as health_router

from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler

from app.core.rate_limit import limiter

app = FastAPI(
    title="Book Management System"
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(user_router)
app.include_router(book_router)
app.include_router(health_router)
