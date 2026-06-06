from datetime import datetime


def validate_book_year(value: int) -> int:
    current_year = datetime.now().year

    if value < 1800 or value > current_year:
        raise ValueError(
            f"Year must be between 1800 and {current_year}"
        )

    return value

def validate_not_blank(value: str) -> str:
    value = value.strip()

    if not value:
        raise ValueError("Field cannot be empty")

    return value