from .. import models, schemas, utils
from fastapi import HTTPException, Depends, APIRouter, status
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import JSON
from ..database import get_db
from typing import Optional

router = APIRouter(
    prefix = "/users",
    tags = ['Users']
)

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CreateUserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# @router.get("/{id}", response_model=schemas.UserOut)
@router.get("/{id}")
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id==id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {id} does not exist")
    # follow_count = db.query(func.count('*')).filter(
    #                         models.followers.c.user_id==id).scalar()
    result = db.query(models.User.id, models.User.email, models.User.username, models.User.created_at, func.count(models.followers.c.user_id).label("followers")).join(
                    models.followers, models.followers.c.user_id == models.User.id, isouter=True).group_by(
                    models.User.id).filter(models.User.id==id).first()
    return result

@router.get("/")
def get_users(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # follow_count = db.query(func.count('*')).filter(
    #                         models.followers.c.user_id==id).scalar()
    result = db.query(models.User.id, models.User.email, models.User.username, models.User.created_at, func.count(models.followers.c.user_id).label("followers")).join(
                    models.followers, models.followers.c.user_id == models.User.id, isouter=True).group_by(
                    models.User.id).filter(models.User.username.contains(search)).limit(limit).offset(skip).all()
    return result