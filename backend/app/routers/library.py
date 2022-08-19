from .. import models, schemas, oauth2 
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, distinct
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db

router = APIRouter(
    prefix = "/libraries",
    tags = ['Libraries']
)

# Get all libraries
# response_model=List[schemas.LibraryOut]
@router.get("/")
def get_libraries(
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user), 
                limit: int = 10, 
                skip: int = 0, 
                search: Optional[str] = ""
                ):
    result_query = db.query(models.Library.id, models.Library.title, models.Library.description, models.Library.owner_id, models.Library.public, models.Library.created_at,
                        func.count(distinct(models.Patron.id)).label("patrons"),
                        func.count(distinct(models.Book.id)).label("books")).join(
                        models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                        models.Book, models.Book.library_id == models.Library.id, isouter=True).group_by(models.Library.id)
    result = result_query.filter(models.Library.title.contains(search)).limit(limit).offset(skip).all()
    return result

# Get my libraries
@router.get("/my-libraries", response_model=List[schemas.LibraryOut])
def get_my_libraries(
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    ):
    pass

# Get library
@router.get("/{id}", response_model=List[schemas.LibraryOut])
def get_library(
                db: Session = Depends(get_db), 
                current_user: int = Depends(oauth2.get_current_user),
                ):
    pass

# Create library
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.LibraryBase)
def create_library(library: schemas.LibraryCreate,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    new_lib = models.Library(owner_id=current_user.id, **library.dict())
    db.add(new_lib)
    db.commit()
    db.refresh(new_lib)
    return new_lib

# Update library
@router.put("/{id}", response_model=schemas.LibraryBase)
def update_library(id: int,
                    updated_library: schemas.LibraryCreate, 
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    library_query = db.query(models.Library).filter(models.Library.id == id)           
    library = library_query.first()
    if library == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {id} does not exit")
    if library.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    library_query.update(updated_library.dict(), synchronize_session=False)
    db.commit()
    return library

# Delete library
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_library(id: int,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    library_query = db.query(models.Library).filter(models.Library.id == id)
    library = library_query.first()
    if library == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {id} does not exit")
    if library.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f"Not authorized to perform requested action")
    library_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)