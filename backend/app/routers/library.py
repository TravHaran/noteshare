from .. import models, schemas, oauth2 
from fastapi import Response, status, HTTPException, Depends, APIRouter, File, UploadFile, Form
from sqlalchemy import func, distinct, and_, desc
from sqlalchemy.orm import Session
from typing import List, Optional
from ..database import get_db
import uuid
from ..config import settings
import os

router = APIRouter(
    prefix = "/api/libraries",
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
                        models.User.username.label('owner'),
                        func.count(distinct(models.Patron.user_id)).label("patrons"),
                        func.count(distinct(models.Book.id)).label("books")).join(
                        models.User, models.User.id == models.Library.owner_id, isouter=True).join(
                        models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                        models.Book, models.Book.library_id == models.Library.id, isouter=True).group_by(
                        models.Library.id, models.User.username)
                        
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
                        models.User.username.label('owner'),
                        func.count(distinct(models.Patron.user_id)).label("patrons"),
                        func.count(distinct(models.Book.id)).label("books")).join(
                        models.User, models.User.id == models.Library.owner_id, isouter=True).join(
                        models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                        models.Book, models.Book.library_id == models.Library.id, isouter=True).filter(models.Library.id.in_(sub_query)).group_by(models.Library.id, models.User.username).order_by(
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
                        models.User.username.label('owner'),
                    func.count(distinct(models.Patron.user_id)).label("patrons"),
                    func.count(distinct(models.Book.id)).label("books")).join(
                        models.User, models.User.id == models.Library.owner_id, isouter=True).join(
                    models.Patron, models.Patron.library_id == models.Library.id, isouter=True).join(
                    models.Book, models.Book.library_id == models.Library.id, isouter=True).group_by(models.Library.id, models.User.username)
    result = result_query.filter(models.Library.id==id).first()
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {id} does not exist")
    return result

# Get my libraries
# , response_model=List[schemas.LibraryOut]
@router.get("/mine/")
def get_my_libraries(
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user),
                    ):
    sub_query = db.query(models.Patron.library_id).where(models.Patron.user_id == current_user.id)
    query = db.query(models.Library,
                        func.count(distinct(models.Patron.user_id)).label("patrons"),
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
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_library(
                    title: str = Form(...),
                    description: str = Form(...),
                    public: bool = Form(...),
                    banner: Optional[UploadFile] = File(None),
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # store the banner image in file system
    if banner:
        print(banner.filename)
        ext = [".jpg", ".jpeg", ".png", ".webp"]
        if not banner.filename.endswith(tuple(ext)):
            raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                    detail="unsupported file-type, please upload either ['.jpg', '.jpeg', '.png', '.webp']")
        banner_ext = banner.filename.split(".")[-1]
        filename = str(uuid.uuid4()) + "." + banner_ext
        content = await banner.read()
        file_location = f"{settings.banner_dir}/{filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(content)
            file_object.close()
    else:
        file_location = f"{settings.default_banner}"
    
    new_lib = models.Library(owner_id=current_user.id, 
                            banner=file_location, 
                            title=title, 
                            description=description, 
                            public=public)
    db.add(new_lib)
    db.commit()
    db.refresh(new_lib)
    # Add user as librarian for this respective library in the patrons table
    # first get the library id 
    library = new_lib.__dict__
    library_id = library['id']
    new_patron = models.Patron(user_id=current_user.id, library_id=library_id, admin_level="librarian")
    db.add(new_patron)
    db.commit()
    db.refresh(new_patron)
    return {"message": f"library of id {library_id} successfully created"}

# Update library
@router.put("/{id}")
async def update_library(id: int,
                    title: Optional[str] = Form(None),
                    description: Optional[str] = Form(None),
                    public: Optional[bool] = Form(None),
                    banner: Optional[UploadFile] = File(None), 
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
    
    # store the banner image in file system
    print(banner.filename)
    ext = [".jpg", ".jpeg", ".png", ".webp"]
    if not banner.filename.endswith(tuple(ext)):
        raise HTTPException(status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                                detail="unsupported file-type, please upload either ['.jpg', '.jpeg', '.png', '.webp']")
    banner_ext = banner.filename.split(".")[-1]
    filename = str(uuid.uuid4()) + "." + banner_ext
    content = await banner.read()
    file_location = f"{settings.banner_dir}/{filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(content)
        file_object.close()

    updated_library_dict = {'title': title,
                            'description': description,
                            'public': public,
                            'banner': file_location}
    library_query.update(updated_library_dict, synchronize_session=False)
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
    # Now we must delete the banner from the filesystem
    try:
        os.remove(library.banner)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"Unable to delete banner from library with id {id}")
    # if file-system deletion was successful we can proceed and delete its data from the database
    library_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)