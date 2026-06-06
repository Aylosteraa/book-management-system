from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_current_user
from app.db.database import get_db

from app.models.user_model import User

from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository

from app.schemas.book_schema import BookCreate, BookResponse, BookUpdate, BookListResponse, BookFilters

from app.services.book_service import BookService

router = APIRouter(
    prefix="/books",
    tags=["Books"]
)


def get_book_service(db: AsyncSession) -> BookService:

    return BookService(
        book_repository=BookRepository(db),
        author_repository=AuthorRepository(db),
    )


@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book(payload: BookCreate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = get_book_service(db)
    book = await service.create_book(payload)

    return BookResponse(
        id=book.id,
        title=book.title,
        author=book.author.name,
        genre=book.genre,
        year=book.year,
    )

@router.get("/{book_id}", response_model=BookResponse)
async def get_book( book_id: UUID, db: AsyncSession = Depends(get_db),):

    service = get_book_service(db)
    book = await service.get_book(book_id)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return BookResponse(
        id=book.id,
        title=book.title,
        author=book.author.name,
        genre=book.genre,
        year=book.year,
    )

@router.patch("/{book_id}", response_model=BookResponse)
async def update_book(book_id: UUID, payload: BookUpdate, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user),):

    service = get_book_service(db)
    book = await service.update_book(book_id, payload)

    if not book:
        raise HTTPException(status_code=404, detail="Book not found")

    return BookResponse(
        id=book.id,
        title=book.title,
        author=book.author.name,
        genre=book.genre,
        year=book.year,
    )

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(book_id: UUID, db: AsyncSession = Depends(get_db), current_user: User = Depends(get_current_user)):

    service = get_book_service(db)
    deleted = await service.delete_book(book_id)

    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    

@router.get("/", response_model=BookListResponse)
async def list_books(filters: BookFilters = Depends(), db: AsyncSession = Depends(get_db),):
    service = get_book_service(db)
    return await service.list_books(filters)
