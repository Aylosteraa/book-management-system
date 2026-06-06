from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.author_model import Author


class AuthorRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_by_name(self, name: str) -> Author | None:

        stmt = select(Author).where(Author.name == name)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create(self, name: str) -> Author:

        author = Author(name=name)
        
        self.db.add(author)

        await self.db.flush()

        return author