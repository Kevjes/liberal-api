from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.departments.models import DepartmentModel
import uuid

class DepartmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[DepartmentModel]:
        result = await self.db.execute(select(DepartmentModel).options(
            selectinload(DepartmentModel.apps),
        ))
        return list(result.unique().scalars().all())
        
    async def get_by_name(self, name: str) -> DepartmentModel | None:
        result = await self.db.execute(select(DepartmentModel).filter(DepartmentModel.name == name))
        return result.scalars().first()
    
    async def get_by_id(self, id: uuid.UUID) -> DepartmentModel | None:
        result = await self.db.execute(select(DepartmentModel).filter(DepartmentModel.id == id))
        return result.scalars().first()
        
    async def create(self, model: DepartmentModel) -> DepartmentModel:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model
    
    async def update(self, model: DepartmentModel) -> DepartmentModel:
        persistent_model = await self.db.merge(model)
        await self.db.commit()
        await self.db.refresh(persistent_model)
        return persistent_model
    
    async def delete(self, model: DepartmentModel) -> None:
        await self.db.delete(model)
        await self.db.commit()
        
        