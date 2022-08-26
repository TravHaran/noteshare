from unittest import result
from .. import models, schemas, utils, oauth2
from fastapi import HTTPException, Depends, APIRouter, status, Response
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/followers",
    tags = ['Followers']
)

# Get all the followers for current user
@router.get("/followers")
def get_my_followers(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    followers_query = db.query(models.followers.c.follower_id,
                                models.User.username,
                                models.User.email).join(
                                models.User, models.User.id==models.followers.c.follower_id, isouter=True).filter(
                                models.followers.c.user_id==current_user.id) 
    results = followers_query.all()
    return results

# Get all the users that a user is following
@router.get("/following")
def get_users_im_following(db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    followers_query = db.query(models.followers.c.user_id,
                                models.User.username,
                                models.User.email).join(
                                models.User, models.User.id==models.followers.c.user_id, isouter=True).filter(
                                models.followers.c.follower_id==current_user.id) 
    results = followers_query.all()
    return results


# Follow a user
@router.post("/{id}")
def follow_user(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # First check if the user exists
    user_query = db.query(models.User).filter(models.User.id==id)
    target_user = user_query.first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    # Make sure user isn't trying to follow themselves
    if id == current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"current user id of {current_user.id} matches with target follower {id}, you cannot follow yourself!")
    # Check if the current user is already following the target user
    following_query = db.query(models.followers).filter(models.followers.c.user_id==id, models.followers.c.follower_id==current_user.id)
    following = following_query.first()
    if following:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user of id {current_user.id} is already following user with id {id}")
    # get current user
    user = db.query(models.User).filter(models.User.id==current_user.id).first()
    target_user.followers.append(user)
    db.add(target_user)
    db.commit()
    return Response(status_code=status.HTTP_201_CREATED)

# Unfollow a user
@router.delete("/{id}")
def unfollow_user(id: int,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    # First check if the user exists
    user_query = db.query(models.User).filter(models.User.id==id)
    target_user = user_query.first()
    if not target_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"user with id: {id} does not exist")
    # Make sure user isn't trying to unfollow themselves
    if id == current_user.id:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"current user id of {current_user.id} matches with target follower {id}, you cannot unfollow yourself!")
    # Check if the current user is following the target user
    following_query = db.query(models.followers).filter(models.followers.c.user_id==id, models.followers.c.follower_id==current_user.id)
    following = following_query.first()
    if not following:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"user of id {current_user.id} is not following user with id {id}, you can't unfollow someone you're not currently following!")
    # get current user
    user = db.query(models.User).filter(models.User.id==current_user.id).first()
    target_user.followers.remove(user)
    db.add(target_user)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)