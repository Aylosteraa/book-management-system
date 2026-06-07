import csv
from io import StringIO

from pydantic import ValidationError

from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository

from app.models.genre_enum import GenreEnum
from app.schemas.book_schema import BookCreate
from app.services.book_service import BookService


class ExportImportService:

    def __init__(self, book_repository: BookRepository, author_repository: AuthorRepository):
        self.book_repository = book_repository
        self.author_repository = author_repository
      
    async def export_books(self):
        books = await self.book_repository.get_all()
        
        output = StringIO()
        writer = csv.writer(output)

        writer.writerow(
            [
                "title",
                "author",
                "genre",
                "year"
            ]
        )

        for book in books:
            writer.writerow(
                [
                    book.title,
                    book.author.name,
                    book.genre.value,
                    book.year,
                ]
            )

        output.seek(0)
        return output.getvalue()
    
    async def import_books(self, content: str):

        reader = csv.DictReader(StringIO(content))

        imported = 0
        failed = 0
        errors = []

        book_service = BookService(
            book_repository=self.book_repository,
            author_repository=self.author_repository,
        )

        for row_number, row in enumerate(reader, start=2):

            try:
                payload = BookCreate(
                    title=row["title"],
                    author=row["author"],
                    genre = GenreEnum(row["genre"].strip().lower()),
                    year=int(row["year"]),
                )

                await book_service.create_book(payload)

                imported += 1

            except ValidationError as e:
                failed += 1
                errors.append(f"Row {row_number}: {e.errors()[0]['msg']}")

            except ValueError as e:
                failed += 1
                errors.append(f"Row {row_number}: {str(e)}")

        return {
            "imported": imported,
            "failed": failed,
            "errors": errors,
        }