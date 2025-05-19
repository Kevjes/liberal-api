from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..users.models import UserModel
from .schemas import UserCreate

class AuthRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> UserModel | None:
        result = await self.session.execute(select(UserModel).filter(UserModel.email == email))
        return result.scalars().first()

    async def create_user(self, user_data: UserCreate, password: str, is_admin: bool = False) -> UserModel:
        user = UserModel(
            email=user_data.email,
            hashed_password=password,
            is_admin=is_admin,
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def update_password(self, user: UserModel, new_password: str) -> None:
        user.hashed_password = new_password
        await self.session.commit()