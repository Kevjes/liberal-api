from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.features.cards.repository import CardRepository
from app.features.cards.services import CardService

def get_cards_service(db: AsyncSession = Depends(get_db)) -> CardService:
    return CardService(CardRepository(db))