from uuid import UUID

from sqlalchemy.exc import IntegrityError

from app.models.book_model import Book

from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository

from app.schemas.book_schema import BookCreate, BookUpdate, BookFilters, BookListResponse, BookResponse

class BookService:

    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository

    async def create_book(self, payload: BookCreate) -> Book:

        author = await (self.author_repository.get_by_name(payload.author))

        if not author:
            author = await (self.author_repository.create(payload.author))

        book = Book(
            title=payload.title,
            genre=payload.genre,
            year=payload.year,
            author_id=author.id
        )

        try:

            book = await (self.book_repository.create(book))

            await self.book_repository.db.commit()
            await self.book_repository.db.refresh(book)

            book.author = author

            return book

        except IntegrityError:

            await self.book_repository.db.rollback()
            raise ValueError("Failed to create book")
        
    
    async def get_book(self, book_id: UUID) -> Book | None:
        return await (self.book_repository.get_by_id(book_id))
    
    async def delete_book(self, book_id: UUID):

        book = await (self.book_repository.get_by_id(book_id))

        if not book:
            return None

        await self.book_repository.delete(book)
        await self.book_repository.db.commit()

        return True
    

    async def update_book(self, book_id: UUID, payload: BookUpdate):

        book = await (self.book_repository.get_by_id(book_id))

        if not book:
            return None
        
        if payload.title is not None:
            book.title = payload.title

        if payload.year is not None:
            book.year = payload.year

        if payload.author is not None:

            author = await (self.author_repository.get_by_name(payload.author))

            if not author:
                author = await (self.author_repository.create(payload.author))

            book.author_id = author.id

        await self.book_repository.db.commit()
        await self.book_repository.db.refresh(book)

        return book
    

    async def list_books(self, filters: BookFilters) -> BookListResponse:
        books, total = await (self.book_repository.list_books(filters))

        total_pages = (total + filters.page_size - 1) // filters.page_size

        return BookListResponse(
            books=[
                BookResponse(
                    id=book.id,
                    title=book.title,
                    author=book.author.name,
                    genre=book.genre,
                    year=book.year,
                )
                for book in books
            ],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
            total_pages=total_pages,
        )
