# backend/app/schemas/user.py
from pydantic import BaseModel, EmailStr
from pydantic import ConfigDict

class UserCreate(BaseModel):
    email: EmailStr
    name: str
    
class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str

    model_config = ConfigDict(from_attributes=True)