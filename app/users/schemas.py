from pydantic import BaseModel, ConfigDict, EmailStr, Field
from datetime import datetime

class UserLoginSchema(BaseModel):
    username: str
    password: str

class UserAddSchema(UserLoginSchema):
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str | None = Field(default=None)

class SafelyUserSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)
    
    id: int
    username: str
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str | None = Field(default=None)
    created_at: datetime
    is_active: bool

class UserSchema(BaseModel):
    model_config = ConfigDict(strict=True, from_attributes=True)
    
    id: int
    username: str
    password: bytes
    email: EmailStr
    last_name: str
    first_name: str
    middle_name: str | None = Field(default=None)
    created_at: datetime
    is_active: bool
