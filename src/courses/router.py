from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db

from src.courses.crud import *
from src.courses.schemas import NewClass, NewEvent


course = APIRouter()


@course.get("/courses", tags=["courses"])
def get_courses(db: Session = Depends(get_db)):
    courses = all_courses(db)
    return courses


@course.get("/courses/{course_id}", tags=["courses"])
def get_course(course_id: str, db: Session = Depends(get_db)):
    course = get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@course.get("/courses/{course_id}/modules", tags=["courses"])
def get_modules_by_course(course_id: str, db: Session = Depends(get_db)):
    modules = get_modules_by_course_id(db, course_id)
    return modules


@course.get("/courses/{course_id}/modules/{module_id}/classes/{class_id}", tags=["courses"])
def get_class_by_id_course_and_module(course_id: str, module_id: str, class_id: str, db: Session = Depends(get_db)):
    return get_module_class(db, course_id, module_id, class_id)


@course.post("/course/{course_id}/modules/{module_id}/classes", tags=["courses"])
def add_new_class_module(course_id: str, module_id: str, new_class: NewClass, db: Session = Depends(get_db)):
    add_class_to_module(db, course_id, module_id, new_class)


@course.get("/course/{course_id}/events/{event_id}", tags=["events"])
def get_event(course_id: str, event_id: str, db: Session = Depends(get_db)):
    event = get_event_by_id(db, event_id)
    if event is None:
        raise HTTPException('Could not find event')
    return event


@course.get("/course/{course_id}/events", tags=["events"])
def get_course_events(course_id: str, db: Session = Depends(get_db)) :
    return get_all__course_events(db, course_id)


@course.post("/course/{course_id}/events", tags=["events"])
def add_event_to_course(course_id: str, event: NewEvent, db: Session = Depends(get_db)):
    return add_new_event_to_course(db, course_id, event)


@course.put("/course/{course_id}/events/{event_id}", tags=["events"])
def add_event_to_course(event_id: str, new_event_data: NewEvent, db: Session = Depends(get_db)):
    return update_event(db, event_id, new_event_data)


@course.delete("/course/{course_id}/events/{event_id}", tags=["events"])
def delete_course_event(course_id: str, event_id: str, db: Session = Depends(get_db)) :
    return delete_event_by_id(db, event_id)
