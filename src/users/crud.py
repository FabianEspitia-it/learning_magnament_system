from fastapi import HTTPException

from sqlalchemy.orm import Session, joinedload

from src.models import User, UserClass
from src.utils.validations import check_email

def get_user_by_id(db: Session, user_id: int) -> User:
    user: User = db.query(User).filter(User.id == user_id).first()
    return user


def add_new_user(db: Session, user_email: str) -> User:
    if not check_email(user_email) or get_user_by_email(user_email) is not None:
        raise HTTPException(status_code= 400, detail='User already exists')
    user: User = User(email=user_email)
    db.add(user)
    db.commit()
    return user


def update_user_by_id(db: Session, user_id: int, new_user: User) -> User:
    pass


def delete_user(db: Session, user_id: int) -> User:
    pass


def get_user_by_email(user_email: str, db: Session) -> User:
    return db.query(User).filter(User.email == user_email).first()

def mark_class_seen_user(user_email: str, class_id: int, db: Session):
    user: User = db.query(User).filter(User.email == user_email).first()
    user_class = UserClass(user_id=user.id, class_id=class_id)
    db.add(user_class)
    db.commit()
    return user_class