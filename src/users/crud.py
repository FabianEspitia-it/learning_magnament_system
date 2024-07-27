from fastapi import HTTPException

from sqlalchemy.orm import Session

from src.models import *
from src.utils.validations import check_email

from src.courses.crud import get_modules_by_course_id

def get_user_by_id(db: Session, user_id: int) -> User:
    user: User = db.query(User, Role.name.label('role_name')).join(Role, User.role_id == Role.id).filter(User.id == user_id).first()
    return user


def add_new_user(db: Session, user_email: str) -> User:
    if not check_email(user_email) or get_user_by_email(user_email, db) is not None:
        raise HTTPException(status_code= 400, detail='User already exists')
    user: User = User(email=user_email, role_id=1)
    db.add(user)
    db.commit()
    return user


def get_all_users(db:Session):
    return db.query(User).all()


def update_user_by_id(db: Session, user_id: int, new_user: User) -> User:
    pass


def delete_user(db: Session, user_id: int) -> User:
    pass


def get_user_by_email(user_email: str, db: Session):
    user_with_role = db.query(User, Role.name.label('role_name')).join(Role, User.role_id == Role.id).filter(User.email == user_email).first()
    
    if user_with_role:
        user, role_name = user_with_role
        user_dict = {**user.__dict__, 'role_name': role_name}
        user_dict.pop('_sa_instance_state', None)
        user_dict.pop('role_id', None)
        return user_dict
    return None


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


def get_all_users_with_course_progress(db: Session):
    users: list[User] = db.query(User).all()
    courses: list[Course] = db.query(Course).all()
    result = []
    for user in users:
        for course in courses:
            result.append({
                "user": user.email,
                "course": course.title,
                "progress": calculate_progress(user.email, course.id, db)
            })
    return result


def login_user(user_email: str, db: Session):
    user = get_user_by_email(user_email, db)
    if not user:
        raise HTTPException(status_code=404, detail='User not found')
    return user


