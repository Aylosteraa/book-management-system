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
- Pytest


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

TEST_DATABASE_URL = postgresql+asyncpg://postgres:password@test_db:5432/books_test

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
Negative Year Book,Test Author,fantasy,-100
Empty Genre Book,Test Author,,2020
```
> [!NOTE]
>For testing import you can use files in data_csv

> [!NOTE]
>Import Rules:
>- Invalid rows are skipped and reported
>- Duplicate books are skipped
>- Import continues even if some rows contain errors

## Tests

### Integration Tests
- test_auth.py — registration, login, and token refresh endpoints.
- test_books.py — CRUD operations, filtering, import/export, and book-related endpoints.

### Unit Tests
- test_book_validators.py — validation rules for book data.
- test_schemas.py — Pydantic schema validation and serialization.
- test_security.py — password hashing, password verification, JWT creation and decoding.
- test_validators.py — reusable validation helper functions.

### Run tests 
Run all tests
```bash
docker compose run --rm tests
```

Run a specific test file
```bash
docker compose run --rm tests pytest tests/integration/test_auth.py -v
```

Run a single test
```bash
docker compose run --rm tests pytest tests/integration/test_auth.py::test_register_user -v
```
