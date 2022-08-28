from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, and_, or_, case
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

router = APIRouter(
    prefix = "/comments",
    tags = ['Comments']
)
  

# create a comment on a book
@router.post("/")
def create_comment(comment: schemas.CommentCreate,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    book = db.query(models.Book).filter(models.Book.id == comment.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {comment.book_id} does not exist")    
    new_comment = models.Comment(user_id=current_user.id, **comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# get all comments from a book
@router.get("/{id}")
def get_comments_on_book(id: int,
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user),
                        limit: int = 50, skip: int = 0):
    # check if book exists
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    
    # Supermassive SQL query!!!!
    # first get the library_id of the current book
    library_id = db.query(models.Book.library_id).filter(models.Book.id==id).first()[0]
    comment_query = db.query(models.Comment,
                            models.User.username.label('owner'),
                            models.Patron.admin_level,
                            case((and_((models.CommentVote.dir==1),(models.CommentVote.user_id==current_user.id)), True), else_=False).label('liked'),
                            case((and_((models.CommentVote.dir==-1),(models.CommentVote.user_id==current_user.id)), True), else_=False).label('disliked'),
                            func.sum(case((models.CommentVote.dir==1, 1), else_=0)).label('likes'),
                            func.sum(case((models.CommentVote.dir==-1, 1), else_=0)).label('dislikes')).join(
                            models.User, models.Comment.user_id==models.User.id, isouter=True).join(
                            models.CommentVote, models.Comment.id==models.CommentVote.comment_id, isouter=True).join(
                            models.Patron, and_((models.Comment.user_id==models.Patron.user_id), (models.Patron.library_id==library_id)), isouter=True).filter(
                            models.Comment.book_id==id).group_by(models.User.username, 
                                                                models.Comment.id, 
                                                                models.CommentVote.user_id, 
                                                                models.CommentVote.dir, 
                                                                models.Patron.admin_level)
    results = comment_query.order_by(models.Comment.created_at.desc()).limit(limit).offset(skip).all()
    return results

@router.put("/{id}")
def edit_comment(id: int,
                updated_comment: schemas.CommentCreate,
                db: Session = Depends(get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id==id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} does not exit")
    if comment.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    comment_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return comment

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(id: int,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id==id)
    comment = comment_query.first()
    if comment == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"comment with id: {id} does not exit")
    # only the author/librarian of the library of the book in which this comment was made, can delete a comment aside from the owner of the comment
    if comment.user_id != current_user.id:
        subquery = db.query(models.Book.library_id).filter(models.Book.id == comment.book_id)
        admin_check = db.query(models.Patron).filter(and_(
            models.Patron.user_id == current_user.id,
            or_(models.Patron.admin_level == "author", models.Patron.admin_level == "librarian"), 
            models.Patron.library_id.in_(subquery)))
        if admin_check == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you don't have admin access to delete comment with id {id}")
    comment_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

