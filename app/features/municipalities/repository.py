from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.municipalities.models import MunicipalityModel
import uuid

class MunicipalityRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[MunicipalityModel]:
        result = await self.db.execute(select(MunicipalityModel).options(
            selectinload(MunicipalityModel.apps),
        ))
        return list(result.unique().scalars().all())
        
    async def get_by_name(self, name: str) -> MunicipalityModel | None:
        result = await self.db.execute(select(MunicipalityModel).filter(MunicipalityModel.name == name))
        return result.scalars().first()
    
    async def get_by_id(self, id: uuid.UUID) -> MunicipalityModel | None:
        result = await self.db.execute(select(MunicipalityModel).filter(MunicipalityModel.id == id))
        return result.scalars().first()
        
    async def create(self, model: MunicipalityModel) -> MunicipalityModel:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model
    
    async def update(self, model: MunicipalityModel) -> MunicipalityModel:
        persistent_model = await self.db.merge(model)
        await self.db.commit()
        await self.db.refresh(persistent_model)
        return persistent_model
    
    async def delete(self, model: MunicipalityModel) -> None:
        await self.db.delete(model)
        await self.db.commit()
        
        