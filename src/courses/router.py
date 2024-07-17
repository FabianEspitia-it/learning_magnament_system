from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db

from src.courses.crud import *


course = APIRouter()


@course.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = all_courses(db)
    return courses


@course.get("/courses/{course_id}")
def get_course(course_id: int, db: Session = Depends(get_db)):
    course = get_course_by_id(db, course_id)
    if course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return course


@course.get("/courses/{course_id}/modules")
def get_modules_by_course(course_id: int, db: Session = Depends(get_db)):
    modules = get_modules_by_course_id(db, course_id)
    return modules


@course.get("/courses/{course_id}/modules/{module_id}/classes/{class_id}")
def get_class_by_id_course_and_module(course_id: int, module_id: int, class_id: int, db: Session = Depends(get_db)):
    return get_module_class(db, course_id, module_id, class_id)

