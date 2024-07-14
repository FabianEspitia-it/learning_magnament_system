from sqlalchemy.orm import Session, joinedload

from src.models import *


def all_courses(db: Session):
    return db.query(Course).all()


def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_modules_by_course_id(db: Session, course_id: int):
    return db.query(Module).filter(Module.course_id == course_id).options(joinedload(Module.classes)).all()
