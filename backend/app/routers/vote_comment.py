from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/vote-comment",
    tags=['Vote_Comment']
)

@router.post("/")
def comment_vote(vote: schemas.CommentVote, 
                db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    if vote.dir not in [1, 0, -1]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Vote dir: {vote.dir} is not a valid option, select from [-1, 0, 1]")
    comment = db.query(models.Comment).filter(models.Comment.id == vote.comment_id).first()
    if not comment:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Comment with id: {vote.comment_id} does not exist")
    
    vote_query = db.query(models.CommentVote).filter(models.CommentVote.comment_id == vote.comment_id, models.CommentVote.user_id == current_user.id)
    found_vote = vote_query.first()
    if vote.dir != 0:
        if found_vote:
            if found_vote.dir == vote.dir:
                if vote.dir == 1:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                    detail=f"user {current_user.id} has already liked comment with id {vote.comment_id}")
                elif vote.dir == -1:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                    detail=f"user {current_user.id} has already disliked comment with id {vote.comment_id}")
            vote_query.update(vote.dict(), synchronize_session=False)
            db.commit()
            return {"message": "successfully updated vote"}
        new_vote = models.CommentVote(user_id=current_user.id, comment_id=vote.comment_id, dir=vote.dir)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}