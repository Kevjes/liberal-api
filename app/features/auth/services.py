from datetime import timedelta
from fastapi import HTTPException, status
from app.core.helper import AppHelper
from app.features.auth.repository import AuthRepository
from app.core.config import settings
from app.features.auth.schemas import Token, UserCreate
from app.core.config import settings
from app.features.users.schemas import UsersSchema

class AuthService:
    def __init__(
        self,
        repo: AuthRepository
    ):
        self.repo = repo

    async def get_user_by_email(self, email: str) -> UsersSchema:
        try:
            user = await self.repo.get_user_by_email(email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found"
                )
        except:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found or problem occurred"
                )
        return UsersSchema.model_validate(user)
    
    async def create_user(self, user_data: UserCreate, is_admin: bool = False,) -> Token:
        password = AppHelper.get_password_hash(user_data.password)
        existing_user = await self.repo.get_user_by_email(user_data.email)
        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
        user = await self.repo.create_user(user_data, password, is_admin=is_admin)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User creation failed"
            )
        access_token = AppHelper.create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return Token(access_token=access_token, token_type="bearer", expires_in= settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)
    
    async def login(self, email: str, password: str) -> Token:
        user = await self.repo.get_user_by_email(email)
        if not user or not AppHelper.verify_password(password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect email or password"
            )
        access_token = AppHelper.create_access_token(
            data={"sub": user.email},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        return Token(access_token=access_token, token_type="bearer", expires_in= settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60)

    async def update_password(self, email: str, new_password: str) -> None:
        password = AppHelper.get_password_hash(new_password)
        user = await self.repo.get_user_by_email(email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        return await self.repo.update_password(user, password)