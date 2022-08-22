from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile, Form
from sqlalchemy import func, and_, or_
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from PyPDF2 import PdfMerger, PdfReader
import uuid
from ..config import settings
from ..utils import generate_thumbnail
import os

router = APIRouter(
    prefix = "/books",
    tags = ['Books']
)

@router.post("/")
async def create_book(
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),
                files: list[UploadFile] = File(...),
                book_title: str = Form(...),
                book_description: str = Form(...),
                library: int = Form(...)):
    # check if library exists
    library_check = db.query(models.Library).filter(models.Library.id == library).first()
    if library_check == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {library} does not exist")
    # if so check if the user is a patron in the library
    patron_check = db.query(models.Patron.admin_level).where(and_(models.Patron.user_id == current_user.id, models.Patron.library_id == library)).first()
    if patron_check == None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"you are not a patron in library with id {library}")

    uploaded_files = []
    for item in files:
        print(item.filename)
        if item.filename.endswith(".pdf") == False:
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="unsupported file-type, please upload a pdf")
        filename = str(uuid.uuid4()) + ".pdf"
        content = await item.read()
        if len(files) > 1:
            file_location = f"{settings.waiting_room_file_dir}/{filename}"
        else:
            # save in database
            file_location = f"{settings.file_dir}/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(content)
        uploaded_files.append(file_location)

    if len(uploaded_files) > 1:
        merger = PdfMerger()
        for pdf in uploaded_files:
            merger.append(pdf)
        filename = str(uuid.uuid4()) + ".pdf"
        file_location = f"{settings.file_dir}/{filename}"  # save in database
        merger.write(file_location)
        merger.close()
        # remove the files that were in the waiting room
        for item in uploaded_files:
            os.remove(item)
    
    thumbnail_path = generate_thumbnail(file_location, settings.thumbnail_dir)
    new_book = models.Book(owner_id=current_user.id,
                            title = book_title,
                            description = book_description,
                            library_id=library,
                            file = file_location,
                            thumbnail = thumbnail_path)
    db.add(new_book)
    db.commit()
    db.refresh(new_book)
    return new_book


@router.get("/")
def get_books(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = db.query(models.Book).filter(models.Library.public == True).filter(models.Book.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get("/public")
def get_books(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    sub_query = db.query(models.Library.id).where(models.Library.public==True)
    results = db.query(models.Book).filter(models.Book.library_id.in_(sub_query)).filter(models.Book.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.get("/from-library/{id}")
def get_books_from_library(id: int, db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    results = db.query(models.Book).where(models.Book.library_id == id).filter(models.Book.title.contains(search)).limit(limit).offset(skip).all()
    return results

@router.delete("/{id}")
def delete_book(id: int,
                db: Session = Depends(get_db),
                current_user: int  = Depends(oauth2.get_current_user)):
    # check if book exists
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    # check if user has acces to delete the book
    # They must be either the owner of the book, or an Author/Librarian in which the library was uploaded to.
    if book.owner_id != current_user.id:
        admin_check = db.query(models.Patron).filter(and_(
                        models.Patron.library_id == book.library_id,
                        models.Patron.user_id == current_user.id,
                        or_(models.Patron.admin_level == "author", models.Patron.admin_level == "librarian"))).first()
        if admin_check == None:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you don't have admin access to delete book with id {id}")
    # Now we must delete the book from the filesystem along with its thumbnail
    try:
        # delete pdf file:
        os.remove(book.file)
        # delete it's thumbnail
        os.remove(book.thumbnail)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Unable to delete book with id {id}")
    # if file-system deletion was successful we can proceed and delete its data from the database
    book_query.delete()
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}")
def update_book(id: int,
                updated_book: schemas.BookUpdate,
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user)):
    # check if book exists
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    # Check if user is owner of book
    if book.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"you don't have admin access to update book with id {id}")

    book_query.update(updated_book.dict(), synchronize_session=False)
    db.commit()
    return book_query.first()


