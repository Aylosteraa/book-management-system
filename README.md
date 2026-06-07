# book-management-system

Create `.env` file:

```
POSTGRES_DB=books_db
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres

DATABASE_URL=postgresql+asyncpg://postgres:password@db:5432/books_db

ALEMBIC_DATABASE_URL=postgresql://postgres:password@db:5432/books_db

SECRET_KEY=your-secret-key
ALGORITHM=HS256

ACCESS_TOKEN_EXPIRE_MINUTES=15
REFRESH_TOKEN_EXPIRE_DAYS=30
```