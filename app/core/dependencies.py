from uuid import UUID

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import  decode_token, oauth2_scheme

from app.db.database import get_db

from app.repositories.user_repository import UserRepository


async def get_current_user(token: str = Depends(oauth2_scheme),db: AsyncSession = Depends(get_db)):

    payload = decode_token(token)

    if not payload:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )

    if payload.get("type") != "access":

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token type"
        )

    user_id = payload.get("sub")

    if not user_id:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token payload"
        )

    repository = UserRepository(db)

    user = await repository.get_by_id(UUID(user_id))

    if not user:

        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user