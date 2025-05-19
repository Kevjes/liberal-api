import uuid
from app.core.helper import AppHelper
from app.features.users.repository import UsersRepository
from app.features.users.schemas import PasswordUpdate, UsersSchema, CreateUserSchema, UpdateUserSchema
from app.features.users.models import UserModel
from fastapi import HTTPException, status

class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    async def get_all(self) -> list[UsersSchema]:
        res = await self.repository.get_all()
        return list(UsersSchema.model_validate(re) for re in res)
    
    async def get_all_admins(self) -> list[UsersSchema]:
        res = await self.repository.get_all_admins()
        return list(UsersSchema.model_validate(re) for re in res)
        
    async def get_by_id(self, id: uuid.UUID) -> UsersSchema:
        res = await self.repository.get_by_id(id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found"
            )
        return res
    
    async def get_by_email(self, email: str) -> UsersSchema:
        res = await self.repository.get_by_email(email)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Users not found"
            )
        return res

    async def create(self, schema: CreateUserSchema) -> UsersSchema:
        model = UserModel(**schema.model_dump(exclude_unset=True, exclude_none=True))
        return await self.repository.create(model)

    async def update(self, schema: UpdateUserSchema, user_id: uuid.UUID) -> UsersSchema:
        model = await self.repository.get_by_id(user_id)
        model = UserModel(**schema.model_dump(exclude_unset=True, exclude_none=True), id=user_id)
        return await self.repository.update(model)
    
    async def update_password(self, schema: PasswordUpdate, user_id: uuid.UUID) -> bool:
        user = await self.repository.get_by_id(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        user.hashed_password = AppHelper.get_password_hash(schema.new_password)
        await self.repository.update(user)
        return True
        

    async def delete(self, id: uuid.UUID) -> None:
        model = await self.repository.get_by_id(id)
        return await self.repository.delete(model)
        