import uuid
from fastapi import APIRouter, Depends
from app.core.security import get_current_admin
from app.features.departments.dependencies import get_departments_service
from app.features.departments.services import DepartmentService
from app.features.departments.schemas import DepartmentSchema, CreateDepartmentSchema, UpdateDepartmentSchema
from app.features.users.models import UserModel

router = APIRouter(prefix="/department", tags=["departments"])

@router.get("/all", response_model=list[DepartmentSchema])
async def get_all_departments(service: DepartmentService = Depends(get_departments_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_all()

@router.get("/{id}", response_model=DepartmentSchema)
async def get_department_by_id(id: uuid.UUID, service: DepartmentService = Depends(get_departments_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_by_id(id)

@router.get("/name/{name}", response_model=DepartmentSchema)
async def get_department_by_name(name: str, service: DepartmentService = Depends(get_departments_service)):
  return await service.get_by_name(name)

@router.post("/", response_model=DepartmentSchema)
async def create_department(schema: CreateDepartmentSchema, service: DepartmentService = Depends(get_departments_service)):
  return await service.create(schema)

@router.put("/", response_model=DepartmentSchema)
async def update_departments(schema: UpdateDepartmentSchema, service: DepartmentService = Depends(get_departments_service), admin: UserModel = Depends(get_current_admin)):
  return await service.update(schema)

@router.delete("/{id}")
async def delete_departments(id: uuid.UUID, service: DepartmentService = Depends(get_departments_service), admin: UserModel = Depends(get_current_admin)):
  return await service.delete(id)

