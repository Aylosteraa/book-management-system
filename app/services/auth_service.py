from uuid import UUID

from app.core.security import create_access_token, create_refresh_token, hash_password, verify_password, decode_token

from app.repositories.user_repository import UserRepository


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def register(self, email: str, password: str):

        existing_user = await (self.user_repository.get_by_email(email))

        if existing_user:
            raise ValueError("User already exists")

        return await self.user_repository.create(
            email=email,
            password_hash=hash_password(password)
            )

    async def login(self, email: str, password: str):

        user = await (self.user_repository.get_by_email(email))

        if not user:
            return None

        if not verify_password(password, user.password_hash):
            return None

        access_token = create_access_token(
            {
                "sub": str(user.id)
            }
        )

        refresh_token = create_refresh_token(
            {
                "sub": str(user.id)
            }
        )

        return {
            "access_token": access_token,
            "refresh_token": refresh_token
        }
    

    async def refresh(self, refresh_token: str):

        payload = decode_token(refresh_token)

        if not payload:
            return None

        if payload.get("type") != "refresh":
            return None

        user_id = payload.get("sub")

        if not user_id:
            return None

        user = await self.user_repository.get_by_id(UUID(user_id))

        if not user:
            return None

        return {
            "access_token": create_access_token(
                {
                    "sub": str(user.id)
                }
            ),
            "refresh_token": create_refresh_token(
                {
                    "sub": str(user.id)
                }
            )
        }
    