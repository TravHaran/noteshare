from .. import models, schemas, utils, oauth2
from fastapi import HTTPException, Depends, APIRouter, status, Response
from sqlalchemy.orm import Session
from ..database import get_db

router = APIRouter(
    prefix = "/patron-invites",
    tags = ['Patron_Invites']
)

"""
A patron invite is when a librarian (inviter) invites users (invitees) to join their library.
Users can either be invited as a reader or an author. This is the only way to join a private library.

Case 1:
librarian invites a user to join their public/private library.
The patron invite is simply logged into the database.
The post request will be as follows.
{
    inviter_id: <>,
    invitee_id: <>,
    library_id: <>,
    admin_level: <>,
}

On the other hand the user (invitee) is the one who will receive these patron invites.
We need an endpoint function which returns all the patron invites that a user has received.
The get request will be as follows:
{
    id: <int>,
    user_id: <int>,
    username: <str>,
    library_id: <int>,
    libray_title: <str>,
    admin_level: <str>,
    created_at: <datetime> 
}

Then we need an endpoint function for a user to either approve or deny an invite.
If the invite is approved (1) the user will be added as a patron to the respective library with the respective admin level
If the invite is denied (0) the patron invite will be deleted from the database.
The post request will be as follows:
{
    id: <int>,
    approved: <bool>
}
"""

# patron invite
@router.post("/")
def patron_invite(
                    patron_invite: schemas.PatronInviteCreate,
                    db: Session = Depends(get_db),
                    current_user: int = Depends(oauth2.get_current_user)):
    # first check if the user being invited exists
    user_query = db.query(models.User).filter(models.User.id==patron_invite.patron_id).first()
    if not user_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with id: {patron_invite.patron_id} does not exist")
    # first check if the library exists
    library_query = db.query(models.Library).filter(models.Library.id==patron_invite.library_id).first()
    if not library_query:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Library with id: {patron_invite.library_id} does not exist")
    # check if the current user has admin access to invite someone to the specified library
    # in other words, the current user must the the owner of said library
    librarian_check = db.query(models.Library).filter(models.Library.id == patron_invite.library_id,
                                                        models.Library.owner_id == current_user.id).first()
    if not librarian_check:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f"You must be the owner of library with id {patron_invite.library_id} to invite patrons to it.")
    # then check if the user being invited is already a patron at the invited admin level
    patron_check = db.query(models.Patron).filter(models.Patron.user_id==patron_invite.patron_id,
                                                    models.Patron.library_id==patron_invite.library_id,
                                                    models.Patron.admin_level==patron_invite.admin_level).first()
    if patron_check:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                detail=f"User of id {patron_invite.patron_id} is already has {patron_invite.admin_level} access to library with id {patron_invite.library_id}")
    # if all conditions pass we can simply go forth and create a patron invite in the database
    new_patron_invite = models.PatronInvite(inviter_id=current_user.id,
                                            invitee_id=patron_invite.patron_id,
                                            library_id=patron_invite.library_id,
                                            admin_level=patron_invite.admin_level)
    db.add(new_patron_invite)
    db.commit()
    db.refresh(new_patron_invite)
    return new_patron_invite


# Get patron invites
@router.get("/")
def get_patron_invites(
                        db: Session = Depends(get_db),
                        current_user: int  = Depends(oauth2.get_current_user)):
    initial_check = db.query(models.PatronInvite).filter(models.PatronInvite.invitee_id == current_user.id).all()
    if not initial_check:
        return {"message": "You have no patron invites"}
    
    query = db.query((models.PatronInvite.id).label("invite_id"),
                        (models.User.id).label("user_id"),
                        models.User.username,
                        (models.PatronInvite.admin_level).label("invited admin level"),
                        models.PatronInvite.library_id,
                        models.Library.title,
                        models.PatronInvite.created_at).join(
                        models.User, models.PatronInvite.inviter_id == models.User.id, isouter=True).join(
                        models.Library, models.PatronInvite.library_id == models.Library.id, isouter=True).filter(
                        models.PatronInvite.invitee_id == current_user.id).order_by(models.PatronInvite.created_at.desc())
    result = query.all()
    return result

# Approve or deny a patron invite
@router.put("/")
def respond_to_patron_invite(response: schemas.PatronInviteResponse,
                                db: Session = Depends(get_db),
                                current_user: int = Depends(oauth2.get_current_user)):
    # first check if the target patron invite has been sent to the current user
    patron_invite_query = db.query(models.PatronInvite).filter(models.PatronInvite.id==response.id,
                                                                models.PatronInvite.invitee_id==current_user.id)
    patron_invite = patron_invite_query.first()
    if not patron_invite:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Patron invite with id {response.id} does not exist")
    if response.approved == True:
        # if the user was already a patron in the library then we simply need to update the patron table with their new admin level set to author
        library_id = db.query(models.PatronInvite.library_id).filter(models.PatronInvite.id==response.id).first()[0]
        patron_query = db.query(models.Patron).filter(models.Patron.user_id==current_user.id, models.Patron.library_id==library_id)
        patron = patron_query.first()
        invited_admin_level = db.query(models.PatronInvite.admin_level).filter(models.PatronInvite.id==response.id,
                                                                models.PatronInvite.invitee_id==current_user.id).first()[0]
        if patron:
            # update that patron
            patron_query.update({"admin_level": invited_admin_level}, synchronize_session=False)
            db.commit()
            # delete the patron invite
            patron_invite_query.delete(synchronize_session=False)
            db.commit()
            return patron_query.first()
        else:
            # add the patron
            new_patron = models.Patron(library_id=library_id, user_id=current_user.id, admin_level=invited_admin_level)
            db.add(new_patron)
            db.commit()
            db.refresh(new_patron)
            # delete the patron invite
            patron_invite_query.delete(synchronize_session=False)
            db.commit()
            return new_patron
    else:
        # The patron invite was denied so we delete it
        patron_invite_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)