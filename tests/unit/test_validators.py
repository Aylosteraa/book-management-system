import pytest

from app.utils.validators import validate_book_year, validate_not_blank

def test_validate_book_year_success():

    result = validate_book_year(2020)

    assert result == 2020


def test_validate_book_year_too_small():

    with pytest.raises(ValueError):

        validate_book_year(1500)


def test_validate_not_blank_success():

    result = validate_not_blank(
        "Dune"
    )

    assert result == "Dune"


def test_validate_not_blank_empty():

    with pytest.raises(ValueError):

        validate_not_blank("   ")