from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.models import User, UserClass, Class, Course, Module
from src.utils.validations import check_email

from src.courses.crud import get_modules_by_course_id

def get_user_by_id(db: Session, user_id: int) -> User:
    user: User = db.query(User).filter(User.id == user_id).first()
    return user


def add_new_user(db: Session, user_email: str) -> User:
    if not check_email(user_email) or get_user_by_email(user_email, db) is not None:
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


def mark_class_unseen_user(user_email: str, class_id: int, db: Session):
    user: User = db.query(User).filter(User.email == user_email).first()
    user_class: UserClass = db.query(UserClass).filter(UserClass.class_id == class_id and UserClass.user_id == user.id).first()
    db.delete(user_class)
    db.commit()
    return user_class


def seen_classes_by_user(user_email: str, course_id: int, db: Session):
    user: User = db.query(User).filter(User.email == user_email).first()
    if not user:
        return []
    
    classes = db.query(Class).join(UserClass
    ).filter(
        UserClass.user_id == user.id,
    ).filter(
        UserClass.class_id == Class.id,
    ).all()
    return classes


def calculate_progress(user_email: str, course_id: int, db: Session):
    seen_classes: list[Class] = seen_classes_by_user(user_email, course_id, db)
    modules: list[Module] = get_modules_by_course_id(db, course_id)
    total_classes: list[Class] = []

    for module in modules:
        total_classes = total_classes + module.classes
    
    percentage_progress: int = int(len(seen_classes)) / int(len(total_classes))
    return f"{int(percentage_progress * 100)}%"