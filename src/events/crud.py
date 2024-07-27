from sqlalchemy.orm import Session, joinedload

from src.models import *



def all_events(db: Session):
    return db.query(Event).all()