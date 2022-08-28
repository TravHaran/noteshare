from typing import Optional
from .. import models, schemas, oauth2 
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/api/patrons",
    tags = ['Patrons']
)

# Get all patrons of a library
@router.get("/{id}")
def get_patrons_of_library(id: int,
                db: Session = Depends(get_db),
                limit: int = 10,
                skip: int = 0,
                search: Optional[str] = ""):
    query = db.query(models.Patron, models.User.username).join(models.User, models.Patron.user_id == models.User.id, isouter=True).where(models.Patron.library_id == id)
    result = query.filter(models.User.username.contains(search)).limit(limit).offset(skip).all()
    return result