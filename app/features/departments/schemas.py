from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

class CreateDepartmentSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Department name")

class UpdateDepartmentSchema(BaseModel):
    id: uuid.UUID = Field(..., description="Department ID")
    name: str = Field(..., min_length=3, max_length=50, description="Department name")

class DepartmentSchema(BaseModel):
    id: uuid.UUID
    name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    