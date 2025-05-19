from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

class CreateMunicipalitySchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50, description="Municipality name")
    department_id: uuid.UUID = Field(..., description="Department ID")

class UpdateMunicipalitySchema(BaseModel):
    id: uuid.UUID = Field(..., description="Municipality ID")
    name: str = Field(..., min_length=3, max_length=50, description="Municipality name")
    department_id: uuid.UUID = Field(..., description="Department ID")

class MunicipalitySchema(BaseModel):
    id: uuid.UUID
    name: str
    department_id: uuid.UUID
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    