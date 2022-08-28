from fastapi import status, HTTPException, Depends, APIRouter
from .. import schemas, database, models, oauth2
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/api/vote-book",
    tags=['Vote_Book']
)

# Like/Un-like/Dislike/Un-dislike a book
# based on dir value
# dir = 1 : like
# dir = -1 : dislike
# dir = 0 : remove like/dislike

@router.post("/")
def book_vote(vote: schemas.BookVote,
                db: Session = Depends(database.get_db),
                current_user: int = Depends(oauth2.get_current_user)):
    if vote.dir not in [1, 0, -1]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"Vote dir: {vote.dir} is not a valid option, select from [-1, 0, 1]")
    book = db.query(models.Book).filter(models.Book.id == vote.book_id).first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id: {vote.book_id} does not exist")
    
    vote_query = db.query(models.BookVote).filter(models.BookVote.book_id == vote.book_id, models.BookVote.user_id == current_user.id)
    found_vote = vote_query.first()
    # if user wants to like the book
    if vote.dir != 0: # user wants to either like or dislike book
        if found_vote:
            if found_vote.dir == vote.dir:
                # user has already liked/disliked the book (you can't like or dislike something twice)
                if vote.dir == 1:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                    detail=f"user {current_user.id} has already liked book with id {vote.book_id}")
                elif vote.dir == -1:
                    raise HTTPException(status_code=status.HTTP_409_CONFLICT, 
                                    detail=f"user {current_user.id} has already disliked book with id {vote.book_id}")
            # if user has previously voted on book and their new vote doesnt produce conflict then we need to update the vote
            vote_query.update(vote.dict(), synchronize_session=False)
            db.commit()
            return {"message": "successfully updated vote"}
        # user is voting on book that they havent voted on
        new_vote = models.BookVote(user_id=current_user.id, book_id=vote.book_id, dir=vote.dir)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else: # user wants to un-like / un-dislike a book
        if not found_vote: # check if vote exists
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist")
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}








