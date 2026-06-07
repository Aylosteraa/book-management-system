# book-management-system

## Overview

Book Management System is a REST API built with FastAPI for managing books and authors.

The application supports:

- JWT Authentication
- CRUD operations
- Filtering
- Sorting
- Pagination
- CSV Import/Export
- Docker deployment

## Tech Stack

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy (Async)
- Alembic
- Pydantic
- JWT
- Docker


## Setup

### Clone repository

```bash
git clone <https://github.com/Aylosteraa/book-management-system.git>
cd book-management-system
```

### Create `.env` file:

```
POSTGRES_DB=books_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=password

DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/books_db

ALEMBIC_DATABASE_URL=postgresql://postgres:password@db:5432/books_db

SECRET_KEY=your-secret-key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```

### Docker Setup

Build and start containers:

```bash
docker compose up --build
```

API documentation (Swager):
```text
http://localhost:8000/docs
```

## API Endpoints

### Authentication

Register
```text
POST /user/register
```
Login
```text
POST /user/authorize
```

Returns:
```text
{
  "access_token": "...",
  "refresh_token": "...",
  "token_type": "bearer"
}
```
> [!IMPORTANT]
> Use the access token in the Swagger **Authorize** button.


### Books

Create Book
```text
POST /books
```
> [!NOTE]
> Authentication required.


Get Books
```text
GET /books
```
Supports:
- pagination
- sorting
- filtering


Get Book By ID
```text
GET /books/{book_id}
```


Update Book
```text
PATCH /books/{book_id}
```
> [!NOTE]
> Authentication required.


Delete Book
```
DELETE /books/{book_id}
```
> [!NOTE]
> Authentication required.

### Import / Export

CSV Export
```text
GET /books/export
```
Downloads all books as CSV.
> [!NOTE]
> Authentication required.

CSV Import
```text
POST /books/import
```
Upload CSV file with the following structure:
> [!NOTE]
> Authentication required.

CSV Import Example
```csv
title,author,genre,year
1984,George Orwell,fiction,1949
Dune,Frank Herbert,sci_fi,1965
Harry Potter and the Philosopher's Stone,J.K. Rowling,fantasy,1997
The Shining,Stephen King,horror,1977
Sapiens,Yuval Noah Harari,History,2011
Pride and Prejudice,Jane Austen,romance,1813
Foundation,Isaac Asimov,sci_fi,1951
The Hobbit,J.R.R. Tolkien,fantasy,1937
Steve Jobs,Walter Isaacson,biography,2011
The Martian,Andy Weir,sci_fi,2014
Broken Year Book,Test Author,fiction,3000
Unknown Genre Book,Test Author,mystery,2020
Missing Title,,fiction,2020
Negative Year Book,Test Author,fantasy,-100
Empty Genre Book,Test Author,,2020
```

Import Rules:
- Invalid rows are skipped and reported
- Duplicate books are skipped
- Import continues even if some rows contain errors
