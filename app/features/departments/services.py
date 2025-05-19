from app.features.departments.repository import DepartmentRepository
from app.features.departments.schemas import DepartmentSchema, CreateDepartmentSchema, UpdateDepartmentSchema
from app.features.departments.models import DepartmentModel
from fastapi import HTTPException, status
import uuid

class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    async def get_all(self) -> list[DepartmentSchema]:
        res = await self.repository.get_all()
        return list(DepartmentSchema.model_validate(re) for re in res)
        
    async def get_by_id(self, id: uuid.UUID) -> DepartmentSchema:
        res = await self.repository.get_by_id(id)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        return res
    
    async def get_by_name(self, name: str) -> DepartmentSchema:
        res = await self.repository.get_by_name(name)
        if not res:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Department not found"
            )
        return res

    async def create(self, schema: CreateDepartmentSchema) -> DepartmentSchema:
        model = DepartmentModel(**schema.model_dump())
        return await self.repository.create(model)

    async def update(self, schema: UpdateDepartmentSchema) -> DepartmentSchema:
        model = await self.repository.get_by_id(schema.id)
        model = DepartmentModel(**schema.model_dump(exclude_unset=True))
        return await self.repository.update(model)

    async def delete(self, id: uuid.UUID) -> None:
        model = await self.repository.get_by_id(id)
        return await self.repository.delete(model)
        