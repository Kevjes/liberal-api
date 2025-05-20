from fastapi import APIRouter, Depends, HTTPException, status
from app.core.helper import AppHelper
from app.core.security import get_current_admin, get_current_user
from app.features.users.dependencies import get_users_service
from app.features.users.models import UserModel
from app.features.users.services import UsersService
from app.features.users.schemas import PasswordUpdate, UsersSchema, CreateUserSchema, UpdateUserSchema
import uuid

router = APIRouter(prefix="/user", tags=["users"])

@router.get("/all", response_model=list[UsersSchema])
async def get_all_users(
  service: UsersService = Depends(get_users_service),
  # current_admin: UserModel = Depends(get_current_admin)
):
  return await service.get_all()

@router.get("/admins", response_model=list[UsersSchema])
async def get_all_admin(service: UsersService = Depends(get_users_service), current_admin: UserModel = Depends(get_current_admin)):
  return await service.get_all_admins()

@router.get("/me", response_model=UsersSchema)
async def get_me(service: UsersService = Depends(get_users_service), current_user: UserModel = Depends(get_current_user)):
  return await service.get_by_id(current_user.id)

@router.get("/email", response_model=UsersSchema)
async def get_users_by_email(
  email: str,
  service: UsersService = Depends(get_users_service),
  # current_admin: UserModel = Depends(get_current_admin)
):
  return await service.get_by_email(email)

@router.get("/{id}", response_model=UsersSchema)
async def get_users_by_id(id: uuid.UUID, service: UsersService = Depends(get_users_service), current_admin: UserModel = Depends(get_current_admin)):
  return await service.get_by_id(id)



@router.post("/", response_model=UsersSchema)
async def create_users(schema: CreateUserSchema, service: UsersService = Depends(get_users_service)):
  return await service.create(schema)

@router.put("/", response_model=UsersSchema)
async def update_users(schema: UpdateUserSchema, service: UsersService = Depends(get_users_service), current_user: UserModel = Depends(get_current_user)):
  return await service.update(schema, current_user.id)

@router.patch("/update-password")
async def update_password(schema: PasswordUpdate, service: UsersService = Depends(get_users_service), current_user: UserModel = Depends(get_current_user)):
  if not AppHelper.verify_password(schema.old_password, current_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect old password"
        )
  await service.update_password(schema, current_user.id)
  return {"message": "Password updated successfully"}

@router.delete("/{id}")
async def delete_users(
  id: uuid.UUID, 
  service: UsersService = Depends(get_users_service),
  current_admin: UserModel = Depends(get_current_admin)
):
  return await service.delete(id)

