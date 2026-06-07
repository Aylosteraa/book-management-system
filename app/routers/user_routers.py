from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

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

def get_auth_service(db: AsyncSession) -> AuthService:

    return AuthService(
        user_repository=UserRepository(db)
    )


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegister, db: AsyncSession = Depends(get_db)):

    service = get_auth_service(db)

    try:
        user = await service.register(payload.email, payload.password)

        return user

    except ValueError as e:
        raise HTTPException(status_code=400,detail=str(e))
    

@router.post("/login", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def login(payload: UserLogin, db: AsyncSession = Depends(get_db)):

    service = get_auth_service(db)
    tokens = await service.login(payload.email, payload.password)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return tokens


@router.post("/refresh", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def refresh_token(payload: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):

    service = get_auth_service(db)
    tokens = await service.refresh(payload.refresh_token)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    return tokens


@router.post("/authorize", response_model=TokenResponse, status_code=status.HTTP_200_OK)
async def authorize_login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):

    service = get_auth_service(db)
    tokens = await service.login(email=form_data.username, password=form_data.password)

    if not tokens:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return tokens


