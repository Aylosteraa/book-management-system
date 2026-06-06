from pydantic import BaseModel, Field, field_validator, ConfigDict
from uuid import UUID

from app.models.genre_enum import GenreEnum
from app.utils.validators import validate_book_year, validate_not_blank


class BookCreate(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    author: str = Field(min_length=1, max_length=255)
    genre: GenreEnum
    year: int

    @field_validator("year")
    @classmethod
    def validate_year(cls, value):
        return validate_book_year(value)
    
    @field_validator("title", "author")
    @classmethod
    def validate_not_blank_fields(cls, value):
        return validate_not_blank(value)
    

class BookUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    genre: GenreEnum | None = None
    year: int | None = None

    @field_validator("year")
    @classmethod
    def validate_year(cls, value):

        if value is None:
            return value

        return validate_book_year(value)
    
    @field_validator("title", "author")
    @classmethod
    def validate_not_blank_fields(cls, value):

        if value is None:
            return value
    
        return validate_not_blank(value)


class BookResponse(BaseModel):
    id: UUID
    title: str
    author: str
    genre: GenreEnum
    year: int

    model_config = ConfigDict(from_attributes=True)


class BookListResponse(BaseModel):
    books: list[BookResponse]
    total: int
    page: int
    page_size: int
    total_pages: int