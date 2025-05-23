from typing import Optional
from sqlalchemy import func, select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from app.features.cards.models import CardModel
import uuid

class CardRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def get_all(self) -> list[CardModel]:
        result = await self.db.execute(select(CardModel))
        return list(result.unique().scalars().all())
    
    async def get_all_by_department_id(self, department_id: uuid.UUID) -> list[CardModel]:
        result = await self.db.execute(select(CardModel).filter(CardModel.department_id == department_id))
        return list(result.unique().scalars().all())
    
    async def get_all_by_municipality_id(self, municipality_id: uuid.UUID) -> list[CardModel]:
        result = await self.db.execute(select(CardModel).filter(CardModel.municipality_id == municipality_id))
        return list(result.unique().scalars().all())
    
    async def get_by_id(self, id: uuid.UUID) -> CardModel | None:
        result = await self.db.execute(select(CardModel).filter(CardModel.id == id))
        return result.unique().scalars().first()
    
    async def get_by_id_model(self, id: uuid.UUID) -> Optional[CardModel]:
        stmt = (
            select(CardModel)
            .where(CardModel.id == id)
            .options(
                selectinload(CardModel.department), # Eager load department
                selectinload(CardModel.municipality) # Eager load municipality
            )
        )
        result = await self.db.execute(stmt)
        return result.unique().scalars().one_or_none()
    
    async def get_by_id_with_relations(self, id: uuid.UUID) -> Optional[CardModel]:
        stmt = select(CardModel).options(selectinload(CardModel.department), selectinload(CardModel.municipality)).where(CardModel.id == id)
        res = await self.db.execute(stmt)
        return res.scalar_one_or_none()
    
    async def get_last_card_number(self) -> Optional[int]:
        result = await self.db.execute(select(func.max(CardModel.number)))
        return result.scalar_one_or_none()
        
    async def create(self, model: CardModel) -> CardModel:
        self.db.add(model)
        await self.db.commit()
        await self.db.refresh(model)
        return model
    
    async def update(self, model: CardModel) -> CardModel:
        persistent_model = await self.db.merge(model)
        await self.db.commit()
        await self.db.refresh(persistent_model)
        return persistent_model
    
    async def delete(self, model: CardModel) -> None:
        await self.db.delete(model)
        await self.db.commit()
        
        