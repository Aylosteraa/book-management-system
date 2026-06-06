from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.book_model import Book


class BookRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, book: Book) -> Book:

        self.db.add(book)

        await self.db.flush()

        return book

    async def get_by_id(self, book_id: UUID) -> Book | None:

        stmt = (select(Book).options(selectinload(Book.author)).where(Book.id == book_id))
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def delete(self, book: Book) -> None:

        await self.db.delete(book)