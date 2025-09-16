from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import or_

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserOut, UserCreate, UserListOut

router = APIRouter(prefix="/users", tags=["users"])

@router.get("", include_in_schema=False)
@router.get("/", response_model=UserListOut)
def list_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    q: Optional[str] = Query(None, description="search by email or name (icontains)"),
    sort: str = Query("id", pattern="^(id|email|name|created_at)$"),
    order: str = Query("asc", pattern="^(asc|desc)$"),
):
    query = db.query(User)
    if q:
        query = query.filter(or_(User.email.ilike(f"%{q}%"), User.name.ilike(f"%{q}%")))
    total = query.count()

    sort_map = {
        "id": User.id,
        "email": User.email,
        "name": User.name,
        "created_at": User.created_at,
    }
    col = sort_map.get(sort, User.id)
    order_by = col.asc() if order == "asc" else col.desc()

    offset = (page - 1) * size
    items = query.order_by(order_by).offset(offset).limit(size).all()
    return {"items": items, "total": total, "page": page, "size": size}

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    return u

@router.post("/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def create_user(user_in: UserCreate, db: Session = Depends(get_db)):
    exists = db.query(User).filter(User.email == user_in.email).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")
    u = User(email=user_in.email, name=user_in.name)
    db.add(u)
    db.commit()
    db.refresh(u)
    return u