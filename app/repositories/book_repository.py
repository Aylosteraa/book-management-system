from uuid import UUID

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.book_model import Book
from app.models.author_model import Author


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

    async def list_books(self, filters):
        stmt = (select(Book).join(Author).options(selectinload(Book.author)))

        count_stmt = (select(func.count()).select_from(Book).join(Author))

        if filters.title:
            stmt = stmt.where(Book.title.ilike(f"%{filters.title}%"))
            count_stmt = count_stmt.where(Book.title.ilike(f"%{filters.title}%"))

        if filters.author:
            stmt = stmt.where(Author.name.ilike(f"%{filters.author}%"))
            count_stmt = count_stmt.where(Author.name.ilike(f"%{filters.author}%"))

        if filters.genre:
            stmt = stmt.where(Book.genre == filters.genre)
            count_stmt = count_stmt.where(Book.genre == filters.genre)

        if filters.year_from:
            stmt = stmt.where(Book.year >= filters.year_from)
            count_stmt = count_stmt.where(Book.year >= filters.year_from)

        if filters.year_to:
            stmt = stmt.where(Book.year <= filters.year_to)
            count_stmt = count_stmt.where(Book.year <= filters.year_to)

        sort_columns = {
            "title": Book.title,
            "year": Book.year,
            "created_at": Book.created_at,
        }

        sort_column = sort_columns.get(filters.sort_by,Book.title)

        if filters.sort_order == "desc":
            stmt = stmt.order_by(sort_column.desc())

        else:
            stmt = stmt.order_by(sort_column.asc())

        offset = (filters.page - 1) * filters.page_size
        stmt = stmt.offset(offset).limit(filters.page_size)
        result = await self.db.execute(stmt)

        books = result.scalars().all()
        total = (await self.db.execute(count_stmt)).scalar()

        return books, total
    
    async def get_all(self):
        stmt = (select(Book).options(selectinload(Book.author)).order_by(Book.title))
        result = await self.db.execute(stmt)
        
        return result.scalars().all()
    
    async def exists(self, title: str, author_name: str, year: int) -> bool:
        stmt = (select(Book).join(Author).where(
                Book.title == title,
                Author.name == author_name,
                Book.year == year,
            )
        )
        result = await self.db.execute(stmt)
        return result.first() is not None