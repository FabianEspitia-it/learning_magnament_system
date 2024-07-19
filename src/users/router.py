import pandas as pd
import io

from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse
from starlette.responses import StreamingResponse

from src.database import get_db

from src.users.crud import *

user = APIRouter()

@user.get('/users/{user_id}', tags=["users"])
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@user.post('/users', tags=["users"])
def add_user(user_email: str, db: Session = Depends(get_db)):
    return add_new_user(db, user_email)

@user.put('/users/{user_id}', tags=["users"])
def update_user(user_id: int, user: User = Depends(), db: Session = Depends(get_db)):
    pass

@user.delete('/users/{user_id}', tags=["users"])
def delete_user(user_id: int, user: User = Depends(), db: Session = Depends(get_db)):
    pass


@user.post("/users/classes/{class_id}", tags=["users"])
def update_class_seen_user(user_email: str, class_id: int, db: Session = Depends(get_db)):
    mark_class_seen_user(user_email, class_id, db)
    return JSONResponse(content={"response": "created"}, status_code=201)


@user.delete("/users/classes/{class_id}", tags=["users"])
def update_class_unseen_user(user_email: str, class_id: int, db: Session = Depends(get_db)):
    mark_class_unseen_user(user_email, class_id, db)
    return JSONResponse(content={"response": "deleted"}, status_code=200)


@user.get("/users/course/{course_id}/modules", tags=["users"])
def get_users_seen_classes_in_module(user_email: str, course_id: int, db: Session = Depends(get_db)):
    return seen_classes_by_user(user_email, course_id, db)


@user.get("/users/course/{course_id}/progress", tags=["users"])
def get_course_progress(user_email: str, course_id: int, db: Session = Depends(get_db)):
    return JSONResponse(
        content={"progress": calculate_progress(user_email, course_id, db)},
        status_code=200
        )


@user.get("/users/information/", tags=["users"])
def get_user_information(db: Session = Depends(get_db)):
    users_information = get_all_users_with_course_progress(db= db)
    df = pd.DataFrame([user for user in users_information])

    # Using BytesIO to save the CSV in memory
    buffer = io.BytesIO()
    df.to_csv(buffer, index=False)
    buffer.seek(0)

    return StreamingResponse(buffer, media_type="text/csv", headers={"Content-Disposition": "attachment;filename=users_data.csv"})