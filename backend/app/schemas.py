from pydantic import BaseModel, EmailStr, ValidationError, validator
from datetime import datetime
from typing import Optional

# define api response schemas for validation

############## Users Schemas ##############
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    # followers: Optional[int] = None
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
###########################################

############## Vote Schemas ##############   
class VoteBase(BaseModel):
    dir: int
    # @validator('dir', check_fields=False)
    # def validate_admin_level(cls, v):
    #     options = [-1, 0, 1]
    #     if v not in options:
    #         raise ValueError(f'invalid vote, please select from valid options: {options}')
    class Config:
        orm_mode = True

class BookVote(BaseModel):
    dir: int
    book_id: int
    
    
class CommentVote(VoteBase):
    user_id: int
    comment_id: int
###########################################

############## Comment Schemas ##############   
class CommentBase(BaseModel):
    book_id: int
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user_id: int
    created_at: datetime
    votes: CommentVote
    owner: UserOut
    class Config:
        orm_mode = True

class CommentOut(BaseModel):
    Comment: Comment
    class Config:
        orm_mode = True
###########################################

############## Book Schemas ##############
class BookBase(BaseModel):
    title: str
    description: str
    file: str
    thumbnail: str
    library_id: int

class BookCreate(BookBase):
    pass

class BookUpdate(BaseModel):
    title: str
    description: str

class Book(BookBase):
    id: int
    created_at: datetime
    owner: UserOut
    ########
    # votes: VoteBook
    # tags: TagOut
    # library: Library
    # owner: UserOut
    ########
    class Config:
        orm_mode = True

class BookOut(BaseModel):
    book: Book
    vote: BookVote
    comment: CommentOut
    class Config:
        orm_mode = True
###########################################

############## Library Schemas ##############
class LibraryBase(BaseModel):
    title: str
    description: str
    public: bool = True

class LibraryCreate(LibraryBase):
    pass

class Library(LibraryBase):
    id: int
    created_at: datetime
    ########
    owner_id: int
    owner: UserOut
    ########
    class Config:
        orm_mode = True

class LibraryOut(BaseModel):
    library: Library
    patrons: int
    books: BookOut
    class Config:
        orm_mode = True
###########################################

############## Follower Schemas ##############
class FollowUser(BaseModel):
    user_id: int

class FollowerOut(BaseModel):
    user: UserOut

class FollowingOut(FollowerOut):
    pass
###########################################

############## Authorization Token Schemas ##############
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
###########################################

############## Tag Schemas ##############
class TagCreate(BaseModel):
    book_id: int
    tag: str

class Tag(BaseModel):
    id: int
    name: str
    created_at: datetime
    class Config:
        orm_mode = True

class TagOut(BaseModel):
    tag: Tag
    class Config:
        orm_mode = True
###########################################

############## PatronRequest Schemas ##############
class PatronRequestBase(BaseModel):
    admin_level = str
    @validator('admin_level', check_fields=False)
    def verify_admin_level(cls, v):
        options = ['author', 'reader']
        if v not in options:
            raise ValueError(f'invalid admin level, please select from valid options: {options}')

class PatronRequestCreate(PatronRequestBase):
    library_id: int

class PatronRequest(PatronRequestBase):
    # User can only use this if they are the librarian of the library to which this request was directed to
    id: int
    ########
    library: Library
    user: UserOut
    ########
    created_at: datetime
    class Config:
        orm_mode = True

class PatronRequestOut(BaseModel):
    request: PatronRequest

class PatronRequestResponse(BaseModel):
    id: int
    approved: bool
###########################################

############## PatronInvite Schemas ##############
class PatronInviteBase(BaseModel):
    admin_level = str
    @validator('admin_level', check_fields=False)
    def verify_admin_level(cls, v):
        options = ['author', 'reader']
        if v not in options:
            raise ValueError(f'invalid admin level, please select from valid options: {options}')

class PatronInviteCreate(PatronInviteBase):
    # this action can only be performed by librarian of library to which aptron is being invited to
    library_id: int
    patron_id: int
    
class PatronInvite(PatronInviteBase):
    id: int
    ########
    user: UserOut
    library: Library
    ########
    created_at: datetime
    class Config:
        orm_mode = True

class PatronInviteOut(BaseModel):
    invite: PatronInvite

class PatronInviteResponse(BaseModel):
    id: int
    approved: bool
###########################################

############## Patron Schemas ##############
class Patrons(BaseModel):
    library_id: int

class Patron(BaseModel):
    id: int
    ########
    user: UserOut
    ########
    admin_level = str
    @validator('admin_level', check_fields=False)
    def validate_admin_level(cls, value):
        options = ['librarian', 'author', 'reader']
        if value not in options:
            raise ValueError(f'invalid admin level, please select from valid options: {options}')
    created_at: datetime

class GetPatronsOut(BaseModel):
    Patron: Patron
###########################################

############## Notification Schemas ##############
class Notifications(BaseModel):
    id: int
    message: str
    created_at: datetime
###########################################
