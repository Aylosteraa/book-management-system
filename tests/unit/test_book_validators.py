import pytest
from pydantic import ValidationError

from app.schemas.book_schema import BookCreate
from app.models.genre_enum import GenreEnum


def test_book_create_success():

    book = BookCreate(
        title="Dune",
        author="Frank Herbert",
        genre="sci_fi",
        year=1965,
    )

    assert book.title == "Dune"
    assert book.author == "Frank Herbert"
    assert book.genre == "sci_fi"
    assert book.year == 1965


def test_book_create_invalid_year_too_small():

    with pytest.raises(ValidationError):

        BookCreate(
            title="Dune",
            author="Frank Herbert",
            genre=GenreEnum.SCI_FI,
            year=1500,
        )


def test_book_create_invalid_year_too_large():

    with pytest.raises(ValidationError):

        BookCreate(
            title="Dune",
            author="Frank Herbert",
            genre="sci_fi",
            year=3000,
        )


def test_book_create_blank_title():

    with pytest.raises(ValidationError):

        BookCreate(
            title="   ",
            author="Frank Herbert",
            genre="sci_fi",
            year=1965,
        )


def test_book_create_blank_author():

    with pytest.raises(ValidationError):

        BookCreate(
            title="Dune",
            author="   ",
            genre="sci_fi",
            year=1965,
        )


def test_book_create_invalid_genre():

    with pytest.raises(ValidationError):

        BookCreate(
            title="Dune",
            author="Frank Herbert",
            genre="invalid_genre",
            year=1965,
        )