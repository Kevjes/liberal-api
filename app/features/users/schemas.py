from typing import Optional
import uuid
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime

class CreateUserSchema(BaseModel):
    email: str
    password: str

class UpdateUserSchema(BaseModel):
    email: Optional[str] = None

class UsersSchema(BaseModel):
    id: uuid.UUID
    email: str
    is_admin: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class PasswordUpdate(BaseModel):
    old_password: str
    new_password: str = Field(min_length=8)
    