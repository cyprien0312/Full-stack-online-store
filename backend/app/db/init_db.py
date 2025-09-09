from sqlalchemy.orm import Session
from app.models.user import User


def init_db(db: Session) -> None:
    # seed an example user if none exists
    if not db.query(User).first():
        demo = User(email="admin@example.com", name="Admin")
        db.add(demo)
        db.commit()


