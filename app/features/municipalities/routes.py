import uuid
from fastapi import APIRouter, Depends
from app.core.security import get_current_admin
from app.features.departments.dependencies import get_departments_service
from app.features.departments.services import DepartmentService
from app.features.municipalities.dependencies import get_municipalities_service
from app.features.municipalities.services import MunicipalityService
from app.features.municipalities.schemas import MunicipalitySchema, CreateMunicipalitySchema, UpdateMunicipalitySchema
from app.features.users.models import UserModel

router = APIRouter(prefix="/municipality", tags=["municipalities"])

@router.get("/all", response_model=list[MunicipalitySchema])
async def get_all_municipalities(service: MunicipalityService = Depends(get_municipalities_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_all()

@router.get("/{id}", response_model=MunicipalitySchema)
async def get_municipality_by_id(id: uuid.UUID, service: MunicipalityService = Depends(get_municipalities_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_by_id(id)

@router.get("/name/{name}", response_model=MunicipalitySchema)
async def get_municipality_by_name(name: str, service: MunicipalityService = Depends(get_municipalities_service)):
  return await service.get_by_name(name)

@router.post("/", response_model=MunicipalitySchema)
async def create_municipality(
  schema: CreateMunicipalitySchema,
  service: MunicipalityService = Depends(get_municipalities_service),
  department_service: DepartmentService = Depends(get_departments_service),
):
  return await service.create(schema, department_service)

@router.put("/", response_model=MunicipalitySchema)
async def update_municipalities(
  schema: UpdateMunicipalitySchema,
  service: MunicipalityService = Depends(get_municipalities_service),
  department_service: DepartmentService = Depends(get_departments_service),
  admin: UserModel = Depends(get_current_admin)
):
  return await service.update(schema, department_service)

@router.delete("/{id}")
async def delete_municipalities(id: uuid.UUID, service: MunicipalityService = Depends(get_municipalities_service), admin: UserModel = Depends(get_current_admin)):
  return await service.delete(id)

