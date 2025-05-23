from app.features.cards.services import CardService
from app.features.departments.services import DepartmentService
from app.features.municipalities.repository import MunicipalityRepository
from app.features.municipalities.schemas import MunicipalitySchema, CreateMunicipalitySchema, UpdateMunicipalitySchema
from app.features.municipalities.models import MunicipalityModel
from fastapi import HTTPException, status
import uuid

class MunicipalityService:
    def __init__(self, repository: MunicipalityRepository):
        self.repository = repository

    async def get_all(self) -> list[MunicipalitySchema]:
        res = await self.repository.get_all()
        return list(MunicipalitySchema.model_validate(re) for re in res)
    
    async def get_all_by_department_id(self, department_id: uuid.UUID) -> list[MunicipalitySchema]:
        res = await self.repository.get_all_by_department_id(department_id)
        return list(MunicipalitySchema.model_validate(re) for re in res)
        
    async def get_by_id(self, id: uuid.UUID) -> MunicipalitySchema:
        res = await self.repository.get_by_id(id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Municipality not found"
            )
        return res
    
    async def get_by_name(self, name: str) -> MunicipalitySchema:
        res = await self.repository.get_by_name(name)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Municipality not found"
            )
        return res

    async def create(self, schema: CreateMunicipalitySchema, department_service: DepartmentService) -> MunicipalitySchema:
        if not await department_service.get_by_id(schema.department_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        if await self.repository.get_by_name(schema.name):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Municipality already exists"
            )
        model = MunicipalityModel(**schema.model_dump())
        return await self.repository.create(model)

    async def update(self, schema: UpdateMunicipalitySchema, department_service: DepartmentService) -> MunicipalitySchema:
        if not await department_service.get_by_id(schema.department_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        model = await self.repository.get_by_id(schema.id)
        model = MunicipalityModel(**schema.model_dump(exclude_unset=True, exclude_defaults=True, exclude_none=True))
        return await self.repository.update(model)

    async def delete(self, id: uuid.UUID, card_service: CardService) -> None:
        if not await card_service.get_all_by_department_id(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department is used by cards"
            )
        model = await self.repository.get_by_id(id)
        return await self.repository.delete(model)
        