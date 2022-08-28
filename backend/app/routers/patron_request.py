from multiprocessing import synchronize
from operator import and_
from .. import models, oauth2, schemas, utils
from fastapi import HTTPException, Response, Depends, APIRouter, status, Form
from sqlalchemy import and_
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/api/patron-requests",
    tags = ['Patron_Requests']
)
""" 
A patron request is when a user requests to join a library
users can request to join as either an author or reader

*** Users cannot make patron requests to private libraries, they must get invited to them! ***

Case 1:
if the request is for reader level and the library is public 
this request will be automatically processed and the user will 
automatically become a patron the library. In this case we don't need to
log the patron request in the patron_requests table as the information 
will be in the patrons table.

Case 2:
if the request is for author level, and the library is 
public, the patron request will be created in the database under 
the patron_requests table.
the post request will be as follows:
{
    user_id: <current_user.id>,
    library_id: <library.owner_id>,
    admin_level: "author",
}


On the other hand a librarian is the one who will receive these patron requests.
We need an end point function which returns all the patron requests that a user has received.
The get request will be as follows:
{
    id: <int>,
    user_id: <int>,
    username: <str>,
    library_id: <int>
    library_title: <str>
    admin_level: "author"
    created_at: <datetime>
}

Then we need an endpoint function for a librarian to either approve or deny the request.
If the request is approved (1) the user will be added as a patron to the respective library at the requested admin level
If the request is denied (0) the patron request will be deleted from the database.
The post request will be as follows:
{
    id: <int>,
    approved: <bool>
}
"""
# patron request
@router.post("/", status_code=status.HTTP_201_CREATED)
def patron_request(
                    patron_request: schemas.PatronRequestCreate,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # first check if the public library exists
    library = db.query(models.Library).filter(models.Library.id==patron_request.library_id, models.Library.public==True).first()
    if not library:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"library with id: {patron_request.library_id} is either private or does not exist")
    patron_check = db.query(models.Patron).filter(models.Patron.user_id==current_user.id,
                                                    models.Patron.library_id==patron_request.library_id,
                                                    (models.Patron.admin_level==patron_request.admin_level) | (models.Patron.admin_level=="librarian")).first()
    if patron_check:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User of id {current_user.id} is either the librarian or already has {patron_request.admin_level} access to library with id {patron_request.library_id}")
    if patron_request.admin_level == "reader":
        # check if the user is already a patron in the library
        patron_check = db.query(models.Patron).filter(models.Patron.user_id==current_user.id,
                                                    models.Patron.library_id==patron_request.library_id,
                                                    models.Patron.admin_level==patron_request.admin_level).first()     
        new_patron = models.Patron(user_id=current_user.id, library_id=patron_request.library_id, admin_level=patron_request.admin_level)
        db.add(new_patron)
        db.commit()
        db.refresh(new_patron)
        return new_patron

    if patron_request.admin_level == "author":
        # get librarian id to assign as requestee_id
        librarian_id = db.query(models.Library.owner_id).filter(models.Library.id==patron_request.library_id).first()[0]
        new_patron_request = models.PatronRequest(requester_id=current_user.id,
                                                    requestee_id=librarian_id,
                                                    library_id=patron_request.library_id, admin_level=patron_request.admin_level)
        db.add(new_patron_request)
        db.commit()
        db.refresh(new_patron_request)
        return new_patron_request
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=f"Unable to process patron request, make sure the patron request was for either author or reader")

# Get patron requests
@router.get("/")
def get_patron_requests(
                        db: Session = Depends(get_db),
                        current_user: int = Depends(oauth2.get_current_user)):
    initial_check = db.query(models.PatronRequest).filter(models.PatronRequest.requestee_id == current_user.id).all()
    if not initial_check:
        return {"message": "You have no patron requests"}
    
    query = db.query((models.PatronRequest.id).label("request_id"),
                        (models.User.id).label("user_id"),
                        models.User.username,
                        (models.PatronRequest.admin_level).label("requested admin level"),
                        models.PatronRequest.library_id,
                        models.Library.title,
                        models.PatronRequest.created_at).join(
                        models.User, models.PatronRequest.requester_id == models.User.id, isouter=True).join(
                        models.Library, models.PatronRequest.library_id == models.Library.id, isouter=True).filter(
                        models.PatronRequest.requestee_id == current_user.id).order_by(models.PatronRequest.created_at.desc())
    result = query.all()
    return result

# Approve or deny a patron request
@router.put("/")
def respond_to_patron_request(
                            response: schemas.PatronRequestResponse,
                            db: Session = Depends(get_db),
                            current_user: int = Depends(oauth2.get_current_user)):
    # first check if the target patron request has been sent to the current user
    patron_request_query = db.query(models.PatronRequest).filter(models.PatronRequest.id==response.id,
                                                                models.PatronRequest.requestee_id==current_user.id)
    patron_request = patron_request_query.first()
    if not patron_request:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patron request with id {response.id} does not exist")
    
    if response.approved == True:
        # if the requester was already a reader in the library then we simply need to update the patron table with their new admin level set to author
        # get requester id
        requester_id = db.query(models.PatronRequest.requester_id).filter(models.PatronRequest.id==response.id).first()[0]
        library_id = db.query(models.PatronRequest.library_id).filter(models.PatronRequest.id==response.id).first()[0]
        patron_query = db.query(models.Patron).filter(models.Patron.user_id==requester_id, models.Patron.library_id==library_id, models.Patron.admin_level=="reader")
        patron = patron_query.first()
        if patron:
            # update that patron
            patron_query.update({"admin_level": "author"}, synchronize_session=False)
            db.commit()
            # delete the patron request
            patron_request_query.delete(synchronize_session=False)
            db.commit()
            return patron_query.first()
        #else the patron_request is for someone to join a library as an author for the first time
        else:
            # add that patron
            new_patron = models.Patron(library_id=library_id, user_id=requester_id, admin_level="author")
            db.add(new_patron)
            db.commit()
            db.refresh(new_patron)
            # delete the patron request
            patron_request_query.delete(synchronize_session=False)
            db.commit()
            return new_patron
    else:
        # The patron request was denied so we delete it
        patron_request_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)



