from typing import Optional
from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
import uuid

from app.features.departments.schemas import DepartmentSchema
from app.features.municipalities.schemas import MunicipalitySchema

class CreateCardSchema(BaseModel):
    first_name: str = Field(..., min_length=3, max_length=50, description="Card first name")
    last_name: str = Field(..., min_length=3, max_length=50, description="Card last name")
    status: str = Field("Membre", min_length=3, max_length=50, description="Card status")
    contact: str = Field(..., min_length=3, max_length=50, description="Card contact")
    email: str = Field(..., pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Card email")
    is_active: bool = Field(False, description="Is card active")
    department_id: uuid.UUID = Field(..., description="Department ID")
    municipality_id: uuid.UUID = Field(..., description="Municipality ID")

class UpdateCardSchema(BaseModel):
    id: uuid.UUID = Field(..., description="Card ID")
    first_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Card first name")
    last_name: Optional[str] = Field(None, min_length=3, max_length=50, description="Card last name")
    status: Optional[str] = Field(None, min_length=3, max_length=50, description="Card status")
    contact: Optional[str] = Field(None, min_length=3, max_length=50, description="Card contact")
    email: Optional[str] = Field(None, pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", description="Card email")
    is_active: Optional[bool] = Field(None, description="Is card active")
    department_id: Optional[uuid.UUID] = Field(None, description="Department ID")
    municipality_id: Optional[uuid.UUID] = Field(None, description="Municipality ID")

class CardSchema(BaseModel):
    id: uuid.UUID
    number: int
    first_name: str
    last_name: str
    contact: str
    status: str
    email: str
    is_active: bool
    image_url: Optional[str] = None
    qr_code: Optional[str] = None
    department: DepartmentSchema
    municipality: MunicipalitySchema
    creator_id: uuid.UUID

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
    