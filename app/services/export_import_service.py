import csv
from io import StringIO

from app.repositories.author_repository import AuthorRepository
from app.repositories.book_repository import BookRepository


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