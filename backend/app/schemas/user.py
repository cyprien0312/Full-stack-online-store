from pydantic import BaseModel, ConfigDict, EmailStr


class UserCreate(BaseModel):
    email: EmailStr
    name: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    model_config = ConfigDict(from_attributes=True)


class UserListOut(BaseModel):
    items: list[UserOut]
    total: int
    page: int
    size: int


class UserUpdate(BaseModel):
    email: EmailStr | None = None
    name: str | None = None
