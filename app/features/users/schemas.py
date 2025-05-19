from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CreateUserSchema(BaseModel):
    first_name: Optional[str] = None
    email: str
    last_name: Optional[str] = None
    password: str

class UpdateUserSchema(BaseModel):
    first_name: Optional[str] = None
    email: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    country: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None

class UsersSchema(BaseModel):
    id: uuid.UUID
    first_name: str
    last_name: str
    email: str
    is_admin: bool
    is_active: bool
    auth_key: str
    phone: Optional[str]
    country: Optional[str]
    city: Optional[str]
    state: Optional[str]
    address: Optional[str]
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)
    