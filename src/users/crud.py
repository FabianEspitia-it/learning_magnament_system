from fastapi import HTTPException

from sqlalchemy.orm import Session, joinedload

from src.models import User
from utils.validations import check_email

async def get_user_by_id(db: Session, user_id: int) -> User:
    return db.query(User).filter(User.id == user_id).first()


async def add_new_user(db: Session, user_email: str) -> User:
    if not check_email(user_email) or get_user_by_email(user_email) is not None:
        raise HTTPException(status_code= 400, detail='User already exists')
    user: User = User(email=user_email)
    db.add(user)
    db.commit()
    return user


async def update_user_by_id(db: Session, user_id: int, new_user: User) -> User:
    pass


async def delete_user(db: Session, user_id: int) -> User:
    pass


async def get_user_by_email(user_email: str, db: Session) -> User:
    return db.query(User).filter(User.email == user_email).first()