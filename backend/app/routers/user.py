import models, schemas, utils
from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)