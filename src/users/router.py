from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.responses import JSONResponse

from src.database import get_db

from src.users.crud import *

user = APIRouter()

@user.get('/users/{user_id}')
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@user.post('/users')
def add_user(user_email: str, db: Session = Depends(get_db)):
    return add_new_user(db, user_email)

@user.put('/users/{user_id}')
def update_user(user_id: int, user: User = Depends(), db: Session = Depends(get_db)):
    pass

@user.delete('/users/{user_id}')
def delete_user(user_id: int, user: User = Depends(), db: Session = Depends(get_db)):
    pass


@user.post("/users/classes/{class_id}")
def update_class_seen_user(user_email: str, class_id: int, db: Session = Depends(get_db)):
    mark_class_seen_user(user_email, class_id, db)
    return JSONResponse(content={"response": "created"}, status_code=201)