from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.features.users.repository import UsersRepository
from app.features.users.services import UsersService

def get_users_service(db: AsyncSession = Depends(get_db)) -> UsersService:
    return UsersService(UsersRepository(db))