from fastapi import status, HTTPException, Depends, APIRouter
import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/like_book",
    tags=['Like_Book']
)