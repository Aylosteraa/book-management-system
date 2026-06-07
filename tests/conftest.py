import sys
import os

import pytest_asyncio

from pathlib import Path
from dotenv import load_dotenv

from httpx import AsyncClient, ASGITransport

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

ROOT_DIR = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT_DIR))

from app.main import app
from app.db.database import Base, get_db

from app.models.user_model import User
from app.models.author_model import Author
from app.models.book_model import Book
from app.core.rate_limit import limiter

load_dotenv()

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

limiter.enabled = False


@pytest_asyncio.fixture
async def engine():

    engine = create_async_engine(
        TEST_DATABASE_URL,
        echo=False,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield engine

    await engine.dispose()


@pytest_asyncio.fixture
async def client(engine):

    SessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )

    async def override_get_db():
        async with SessionLocal() as session:
            yield session

    app.dependency_overrides[get_db] = override_get_db

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as ac:
        yield ac

    app.dependency_overrides.clear()