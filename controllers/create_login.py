from sqlalchemy.orm import Session
import models.schemas as _schemas
from models import models
from auth import auth


def create_user(db: Session, user: _schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.hashed_password)
    db_user = models.Account(
        login=user.login,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

