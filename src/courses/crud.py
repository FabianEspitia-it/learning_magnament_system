from fastapi import HTTPException
from sqlalchemy.orm import Session, joinedload

from src.models import *
from src.courses.schemas import NewClass, NewEvent


def all_courses(db: Session):
    return db.query(Course).all()


def get_course_by_id(db: Session, course_id: int):
    return db.query(Course).filter(Course.id == course_id).first()


def get_modules_by_course_id(db: Session, course_id: int):
    return db.query(Module).filter(Module.course_id == course_id).options(joinedload(Module.classes)).all()


def get_module_by_id(db: Session, course_id: int, module_id: int) -> Class:
    module = db.query(Module).filter(Module.course_id == course_id and Module.id == module_id).options(joinedload(Module.classes)).first()
    if module is None:
        raise HTTPException(status_code=404, detail="Module not found")
    return module


def get_module_class(db: Session, course_id: int, module_id: int, class_id: int):
    module: Module = get_module_by_id(db, course_id, module_id)
    classes: list[Class] = module.classes
    searched_class = list(filter(lambda c: c.id == class_id, classes))
    if len(searched_class) == 0:
        raise HTTPException(status_code=404, detail="Class not found") 
    return searched_class[0]


def add_class_to_module(db: Session, course_id: int, module_id: int, new_class: NewClass):
    class_module = get_module_by_id(db, course_id, module_id)
    class_instance = Class(
        title= new_class.title,
        video_link=new_class.video_link,
        description=new_class.description,
        previous_id=new_class.previous_id,
        next_id=new_class.next_id,
        module_id=new_class.module_id,
        module=class_module
    )
    
    db.add(class_instance)
    db.commit()

    return class_instance


def get_event_by_id(db: Session, event_id: str):
    return db.query(Event).filter(Event.id == event_id).first()


def get_all__course_events(db: Session, course_id: str):
    return db.query(Course).filter(Course.id == course_id).options(joinedload(Course.events)).all()


def add_new_event_to_course(db: Session, course_id: str, new_event: NewEvent):
    course = get_course_by_id(db, course_id)
    
    if course is None:
        raise HTTPException('Course not found', status_code=404)
    
    event = Event(
        title = new_event.title,
        event_date = new_event.date,
        description = new_event.description,
        course_id = course_id,
        course = course
    )

    db.add(event)
    db.commit()

    return event

def update_event(db: Session, event_id: str, new_event_data: NewEvent):
    event = get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException('Event not found', status_code=404)

    for var, value in vars(new_event_data).items():
        setattr(event, var, value) if value else None

    db.add(event)
    db.commit()
    db.refresh(event)

    return event


def delete_event_by_id(db: Session, event_id: str):
    event = get_event_by_id(db, event_id)
    db.delete(event)
    db.commit()
    return event
