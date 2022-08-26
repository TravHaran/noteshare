from .. import models, schemas, oauth2
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile, Form
from fastapi.responses import FileResponse
from sqlalchemy import func, and_, or_, case, literal_column
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
from PyPDF2 import PdfMerger, PdfReader
import uuid
from ..config import settings
from ..utils import generate_thumbnail
import os

router = APIRouter(
    prefix = "/downloads",
    tags = ['Downloads']
)

@router.get("/{id}")
async def download_book(id: int,
                    current_user: int = Depends(oauth2.get_current_user),
                    db: Session = Depends(get_db)):
    # Check if the book exists
    book_query = db.query(models.Book).filter(models.Book.id == id)
    book = book_query.first()
    if book == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"book with id: {id} does not exist")
    # get file path of book
    file_path = db.query(models.Book.file).filter(models.Book.id==id).first()[0]
    file_name = db.query(models.Book.title).filter(models.Book.id==id).first()[0] + ".pdf"
    new_download = models.Download(book_id=id, user_id=current_user.id)
    db.add(new_download)
    db.commit()
    db.refresh(new_download)
    return FileResponse(path=file_path, filename=file_name, media_type='pdf')
    