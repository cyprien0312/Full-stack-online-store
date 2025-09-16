from pydantic import BaseModel, EmailStr, ConfigDict
from typing import List

class UserCreate(BaseModel):
    email: EmailStr
    name: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    model_config = ConfigDict(from_attributes=True)

class UserListOut(BaseModel):
    items: List[UserOut]
    total: int
    page: int
    size: int