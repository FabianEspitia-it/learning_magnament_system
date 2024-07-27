from fastapi import APIRouter, HTTPException, status, Depends


from src.database import get_db

from src.events.crud import *



event = APIRouter()

@event.get('/events', tags=["events"])
def get_all_events(db: Session = Depends(get_db)):
    return all_events(db)