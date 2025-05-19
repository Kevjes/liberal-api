from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.features.municipalities.repository import MunicipalityRepository
from app.features.municipalities.services import MunicipalityService

def get_municipalities_service(db: AsyncSession = Depends(get_db)) -> MunicipalityService:
    return MunicipalityService(MunicipalityRepository(db))