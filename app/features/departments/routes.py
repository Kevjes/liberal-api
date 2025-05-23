import uuid
from fastapi import APIRouter, Depends, HTTPException, status
from app.core.security import get_current_admin
from app.features.cards.dependencies import get_cards_service
from app.features.cards.services import CardService
from app.features.departments.dependencies import get_departments_service
from app.features.departments.services import DepartmentService
from app.features.departments.schemas import DepartmentSchema, CreateDepartmentSchema, UpdateDepartmentSchema
from app.features.municipalities.dependencies import get_municipalities_service
from app.features.municipalities.services import MunicipalityService
from app.features.users.models import UserModel

router = APIRouter(prefix="/department", tags=["departments"])

@router.get("/all", response_model=list[DepartmentSchema])
async def get_all_departments(
  service: DepartmentService = Depends(get_departments_service), 
  # admin: UserModel = Depends(get_current_admin)
):
  return await service.get_all()

@router.get("/{id}", response_model=DepartmentSchema)
async def get_department_by_id(id: uuid.UUID, service: DepartmentService = Depends(get_departments_service), admin: UserModel = Depends(get_current_admin)):
  return await service.get_by_id(id)

@router.get("/name/{name}", response_model=DepartmentSchema)
async def get_department_by_name(name: str, service: DepartmentService = Depends(get_departments_service)):
  return await service.get_by_name(name)

@router.post("/", response_model=DepartmentSchema)
async def create_department(schema: CreateDepartmentSchema, service: DepartmentService = Depends(get_departments_service) , admin: UserModel = Depends(get_current_admin)):
  return await service.create(schema)

@router.put("/", response_model=DepartmentSchema)
async def update_departments(schema: UpdateDepartmentSchema, service: DepartmentService = Depends(get_departments_service), admin: UserModel = Depends(get_current_admin)):
  return await service.update(schema)

@router.delete("/{id}")
async def delete_departments(
  id: uuid.UUID, 
  service: DepartmentService = Depends(get_departments_service),
  municipality_service: MunicipalityService = Depends(get_municipalities_service),
  card_service: CardService = Depends(get_cards_service),
  admin: UserModel = Depends(get_current_admin)
):
  if not await municipality_service.get_all_by_department_id(id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Department has municipalities"
            )
  return await service.delete(id, card_service)

