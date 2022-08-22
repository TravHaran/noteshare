from .. import models, schemas, oauth2 
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func, distinct, and_, desc
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
                limit: int = 10, 
                skip: int = 0, 
                search: Optional[str] = ""
                ):
    result_query = db.query(models.Library,
                        func.count(distinct(models.Patron.id)).label("patrons"),
                        func.count(distinct(models.Book.id)).label("books")).join(
                        models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                        models.Book, models.Book.library_id == models.Library.id, isouter=True).group_by(models.Library.id)
    result = result_query.filter(models.Library.title.contains(search)).limit(limit).offset(skip).all()
    return result

@router.get("/public")
def get_public_libraries(
                db: Session = Depends(get_db), 
                limit: int = 10, 
                skip: int = 0, 
                search: Optional[str] = ""
                ):
    sub_query = db.query(models.Library.id).where(models.Library.public == True)
    query = db.query(models.Library,
                        func.count(distinct(models.Patron.id)).label("patrons"),
                        func.count(distinct(models.Book.id)).label("books")).join(
                        models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                        models.Book, models.Book.library_id == models.Library.id, isouter=True).filter(models.Library.id.in_(sub_query)).group_by(models.Library.id).order_by(
                            desc("patrons"))
    result = query.filter(models.Library.title.contains(search)).limit(limit).offset(skip).all()
    return result

# Get library
@router.get("/{id}")
def get_library(id: int,
                db: Session = Depends(get_db)
                ):
    # result_query = db.query(models.Library.id, models.Library.title, models.Library.description, models.Library.owner_id, models.Library.public, models.Library.created_at,
    #                 func.count(distinct(models.Patron.id)).label("patrons"),
    #                 func.count(distinct(models.Book.id)).label("books")).join(
    #                 models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
    #                 models.Book, models.Book.library_id == models.Library.id, isouter=True).group_by(models.Library.id)
    # result = result_query.filter(models.Library.id==id).first()
    result_query = db.query(models.Library,
                    func.count(distinct(models.Patron.id)).label("patrons"),
                    func.count(distinct(models.Book.id)).label("books")).join(
                    models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                    models.Book, models.Book.library_id == models.Library.id, isouter=True).group_by(models.Library.id)
    result = result_query.filter(models.Library.id==id).first()
    return result

# Get my libraries
# , response_model=List[schemas.LibraryOut]
@router.get("/mine/")
def get_my_libraries(
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    ):
    sub_query = db.query(models.Patron.library_id).where(models.Patron.user_id == current_user.id)
    query = db.query((models.Library.id).label("library_id"), models.Library.title, models.Library.description, models.Library.owner_id, models.Library.public, models.Library.created_at,
                        func.count(distinct(models.Patron.id)).label("patrons"),
                        func.count(distinct(models.Book.id)).label("books")).join(
                        models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                        models.Book, models.Book.library_id == models.Library.id, isouter=True).filter(models.Library.id.in_(sub_query)).group_by(models.Library.id)
    result = query.all()
    return result

@router.get("/my-library-admin-level/{id}")
def get_my_library_admin_level(id: int,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)
                    ):
    result = db.query(models.Patron.admin_level).where(and_(models.Patron.user_id == current_user.id, models.Patron.library_id == id)).first()
    if result == None:
        # either the library doesnt exist
        check = db.query(models.Library).filter(models.Library.id == id).first()
        if check == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {id} does not exist")
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"you are not a patron in library with id {id}")
        # or the user is not a patron of the library
    return result

# Create library
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Library)
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