import uuid
from pydantic import BaseModel, EmailStr, Field

class EmailPasswordRequestForm(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=50, description="User email")
    password: str = Field(..., min_length=8, description="User password")

class UserCreate(BaseModel):
    email: EmailStr = Field(..., min_length=5, max_length=50, description="User email")
    password: str = Field(min_length=8, description="User password")

class UserPublic(BaseModel):
    id: uuid.UUID
    email: EmailStr
    hashed_password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    expires_in: int

class PasswordResetRequest(BaseModel):
    email: EmailStr

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(min_length=8)