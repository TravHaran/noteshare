from .. import models, schemas, utils, oauth2
from fastapi import HTTPException, Depends, APIRouter, status, Form, Response
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/tags",
    tags = ['Tags']
)

# Get all tags for a book
# TODO
@router.get("/{id}")
def get_book_tags(id: int,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # check if the book exists
    book_check = db.query(models.Book).filter(models.Book.id==id)
    book = book_check.first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    query = db.query(models.book_tag_map,
                    models.Tag.name).join(
                    models.Tag, models.Tag.id==models.book_tag_map.c.tag_id, isouter=True).filter(
                    models.book_tag_map.c.book_id==id)
    result = query.all()
    return result

# Get all tags from all books in a library
# TODO
@router.get("/from-library/{id}")
def get_tags_from_library(id: int,
                            db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    # first check if the library exists
    library_query = db.query(models.Library).filter(models.Library.id==id).first()
    if not library_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {id} does not exist")
    sub_query = db.query(models.Book.id).filter(models.Book.library_id==id)
    query = db.query(models.book_tag_map,
                    models.Tag.name).join(
                    models.Tag, models.Tag.id==models.book_tag_map.c.tag_id, isouter=True).filter(
                    models.book_tag_map.c.book_id.in_(sub_query))
    results = query.all()
    return results

# Add tags to a book
# TODO
@router.post("/{id}")
def add_tags(id: int,
            db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user),
            tags: list[str] = Form(...)):
    # check if the book exists
    book_check = db.query(models.Book).filter(models.Book.id==id)
    book = book_check.first()
    if not book:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    # check if the current user is the owner of the book in which they want to add tags to
    owner_check = db.query(models.Book).filter(models.Book.id==id, models.Book.owner_id==current_user.id).first()
    if not owner_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you don't have admin access to add tags to book with id {id}")
    for tag in tags:
        # add tag to tag table
        # check if the tag already exists for the book
        tag_query = db.query(models.Tag.name,
                            models.book_tag_map.c.book_id).join(models.book_tag_map, 
                            models.book_tag_map.c.tag_id == models.Tag.id).filter(models.book_tag_map.c.book_id==id,
                            models.Tag.name==tag).first()
        if tag_query:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"book with id {id} already has the tag: {tag}")
        new_tag = models.Tag(name=tag)
        db.add(new_tag)
        db.commit()
        db.refresh(new_tag)
        book.tags.append(new_tag)
        db.add(book)
        db.commit()
    return Response(status_code=status.HTTP_201_CREATED)

# delete tags from a book
# TODO
@router.delete("/{id}")
def delete_tags(id: int,
            tags: schemas.TagDelete,
            db: Session = Depends(get_db),
            current_user: int = Depends(oauth2.get_current_user)):
    # check if the book exists
    book_check = db.query(models.Book).filter(models.Book.id==id).first()
    if not book_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    # check if the current user is the owner of the book in which they want to delete tags from
    owner_check = db.query(models.Book).filter(models.Book.id==id, models.Book.owner_id==current_user.id).first()
    if not owner_check:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you don't have admin access to delete tags from book with id {id}")
    
    for tag_id in tags.__dict__['tag_ids']:
        tag_query = db.query(models.book_tag_map).filter(models.book_tag_map.c.book_id==id, models.book_tag_map.c.tag_id==tag_id)
        tag = tag_query.first()
        if not tag:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"tag of id: {tag_id} does not exist for book with id: {id}")
        tag_query.delete(synchronize_session=False)
        db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)