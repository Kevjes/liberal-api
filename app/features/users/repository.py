import uuid
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.users.models import UserModel

class UsersRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[UserModel]:
        result = await self.db.execute(select(UserModel))
        return list(result.unique().scalars().all())
    
    async def get_all_admins(self) -> list[UserModel]:
        result = await self.db.execute(select(UserModel).filter(UserModel.is_admin == True))
        return list(result.scalars().all())
        
    async def get_by_id(self, id: uuid.UUID) -> UserModel | None:
        result = await self.db.execute(select(UserModel).filter(UserModel.id == id))
        return result.scalars().first()
    
    async def get_by_email(self, email: str) -> UserModel | None:
        result = await self.db.execute(select(UserModel).filter(UserModel.email == email))
        return result.scalars().first()
        
    async def create(self, model: UserModel) -> UserModel:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model
    
    async def update(self, model: UserModel) -> UserModel:
        persistent_model = await self.db.merge(model)
        await self.db.commit()
        await self.db.refresh(persistent_model)
        return persistent_model
    
    async def delete(self, model: UserModel) -> None:
        await self.db.delete(model)
        await self.db.commit()
        
        