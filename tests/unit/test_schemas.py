import pytest

from pydantic import ValidationError
from app.schemas.book_schema import BookCreate

def test_book_create_schema():
    book = BookCreate(
        title="Dune",
        author="Frank Herbert",
        genre="sci_fi",
        year=1965,
    )

    assert book.title == "Dune"

def test_book_create_invalid_year():

    with pytest.raises(ValidationError):

        BookCreate(
            title="Dune",
            author="Frank Herbert",
            genre="sci_fi",
            year=3000,
        )


def test_book_create_empty_author():

    with pytest.raises(ValidationError):

        BookCreate(
            title="Dune",
            author=" ",
            genre="sci_fi",
            year=1965,
        )

