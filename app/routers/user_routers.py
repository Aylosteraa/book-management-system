from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db

from app.repositories.user_repository import UserRepository

from app.schemas.auth_schema import TokenResponse, RefreshTokenRequest
from app.schemas.user_schema import UserLogin, UserRegister, UserResponse

from app.services.auth_service import AuthService


router = APIRouter(
    prefix="/user",
    tags=["User"]
)

@router.post("/register", response_model=UserResponse)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):

    repository = UserRepository(db)
    service = AuthService(repository)

    try:
        user = await service.register(payload.email, payload.password)

        return user

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):

    repository = UserRepository(db)
    service = AuthService(repository)
    tokens = await service.login(payload.email, payload.password)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return tokens


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):

    repository = UserRepository(db)
    service = AuthService(repository)
    tokens = await service.refresh(payload.refresh_token)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return tokens
