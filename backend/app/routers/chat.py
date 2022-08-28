from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, and_, or_, case
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

router = APIRouter(
    prefix = "/api/chats",
    tags = ['Chats']
)

# Create a chat in a library
@router.post('/')
def create_chat(chat: schemas.ChatCreate, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # Check if library exists
    library_query = db.query(models.Library).filter(models.Library.id == chat.library_id)
    library = library_query.first()
    if library is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Library with id {id} does not exist")
    # Check if user is a patron of the library
    patron_check = db.query(models.Patron.admin_level).where(and_(models.Patron.user_id == current_user.id, models.Patron.library_id == chat.library_id)).first()
    if patron_check == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"you are not a patron in library with id {chat.library_id}")
    
    new_chat  = models.Chat(user_id=current_user.id, **chat.dict())
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)
    return new_chat

@router.get('/{id}')
def get_chats_from_library(id: int, 
                        db: Session = Depends(get_db), 
                        current_user: int = Depends(oauth2.get_current_user), 
                        limit: int = 50, skip: int = 0):
    # Check if library exists
    library_query = db.query(models.Library).filter(models.Library.id == id)
    library = library_query.first()
    if library is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Library with id {id} does not exist")
    # Check if user is a patron of the library
    patron_check = db.query(models.Patron.admin_level).where(and_(models.Patron.user_id == current_user.id, models.Patron.library_id == id)).first()
    if patron_check == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"you are not a patron in library with id {id}")
    
    chats = db.query(models.Chat, models.User.username).join(
    models.User, models.User.id==models.Chat.user_id).filter(models.Chat.library_id==id).order_by(models.Chat.created_at.desc()).limit(limit).offset(skip).all()
    return chats


@router.put('/{id}')
def update_chat(id: int, 
                updated_comment: schemas.ChatCreate,
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    chat_query = db.query(models.Chat).filter(models.Chat.id==id)
    chat = chat_query.first()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"chat with id {id} does not exist")
    if chat.user_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    chat_query.update(updated_comment.dict(), synchronize_session=False)
    db.commit()
    return chat

@router.delete('/{id}')
def delete_chat(id: int, 
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    chat_query = db.query(models.Chat).filter(models.Chat.id==id)
    chat = chat_query.first()
    if chat is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"chat with id {id} does not exist")
    # check if user has acces to delete the chat
    # They must be either the owner of the chat, or an Author/Librarian for the libvrary in which the chat was uploaded to.
    if chat.user_id != current_user.id:
        admin_check = db.query(models.Patron).filter(and_(
                        models.Patron.library_id == chat.library_id,
                        models.Patron.user_id == current_user.id,
                        or_(models.Patron.admin_level == "author", models.Patron.admin_level == "librarian"))).first()
        if admin_check == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you don't have admin access to delete chat with id {id}")
    chat_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


    