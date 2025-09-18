from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import or_
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserListOut, UserOut, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("", include_in_schema=False)
@router.get("/", response_model=UserListOut)
def list_users(
    db: Session = Depends(get_db),
    page: int = Query(1, ge=1),
    size: int = Query(10, ge=1, le=100),
    q: str | None = Query(None, description="search by email or name (icontains)"),
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


@router.put("/{user_id}", response_model=UserOut)
def replace_user(user_id: int, user_in: UserCreate, db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    # 唯一性校验
    exists = db.query(User).filter(User.email == user_in.email, User.id != user_id).first()
    if exists:
        raise HTTPException(status_code=409, detail="Email already exists")
    u.email = user_in.email
    u.name = user_in.name
    db.commit()
    db.refresh(u)
    return u


@router.patch("/{user_id}", response_model=UserOut)
def update_user(user_id: int, user_in: UserUpdate, db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    if user_in.email is not None:
        exists = db.query(User).filter(User.email == user_in.email, User.id != user_id).first()
        if exists:
            raise HTTPException(status_code=409, detail="Email already exists")
        u.email = user_in.email
    if user_in.name is not None:
        u.name = user_in.name
    db.commit()
    db.refresh(u)
    return u


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    u = db.get(User, user_id)
    if not u:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(u)
    db.commit()
    return None
