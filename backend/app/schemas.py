from pydantic import BaseModel, EmailStr, ValidationError, validator
from datetime import datetime
from typing import Optional

# define api response schemas for validation

############## Users Schemas ##############
class UserCreate(BaseModel):
    email: EmailStr
    username: str
    password: str

class CreateUserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    # followers: Optional[int] = None
    created_at: datetime
    class Config:
        orm_mode = True

class UserOut(BaseModel):
    id: int
    email: EmailStr
    username: str
    followers: Optional[int] = None
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
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

############## Library Schemas ##############
class LibraryCreate(BaseModel):
    title: str
    description: str
    public: bool = True

class LibraryBase(BaseModel):
    id: int
    title: str
    description: str
    ########
    owner_id: int
    ########
    public: bool = True
    created_at: datetime
    class Config:
        orm_mode = True

class Library(BaseModel):
    id: int
    title: str
    description: str
    patrons: int
    books: int
    ########
    owner_id: int
    ########
    public: bool = True
    created_at: datetime
    class Config:
        orm_mode = True

class LibraryOut(BaseModel):
    library: Library
###########################################

############## Book Schemas ##############
class BookCreate(BaseModel):
    title: str
    description: Optional[str] = None
    file: str
    library_id: int

class Book(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    file: str
    page_count: int
    likes: int
    dislikes: int
    tags: list
    comments: int
    ########
    library: Library
    owner: UserOut
    ########
    created_at: datetime
    class Config:
        orm_mode = True

class BookOut(BaseModel):
    book: Book
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
class GetPatrons(BaseModel):
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

############## Comment Schemas ##############   
class CommentCreate(BaseModel):
    book_id: int
    content: str

class Comment(BaseModel):
    id: int
    user_id: int
    created_at: datetime
    likes: int
    class Config:
        orm_mode = True

class CommentOut(BaseModel):
    Comment: Comment
###########################################

############## Like Schemas ##############   
class VoteBase(BaseModel):
    dir: int
    @validator('dir', check_fields=False)
    def validate_admin_level(cls, v):
        options = [-1, 0, 1]
        if v not in options:
            raise ValueError(f'invalid vote, please select from valid options: {options}')

class VoteBook(VoteBase):
    book_id: int

class VoteComment(VoteBase):
    comment_id: int
###########################################

############## Tag Schemas ##############
class TagCreate(BaseModel):
    book_id: int
    tag: str

class Tag(BaseModel):
    id: int
    name: str
    created_at: datetime

class TagOut(BaseModel):
    tag: Tag
###########################################

############## Notification Schemas ##############
class Notifications(BaseModel):
    id: int
    message: str
    created_at: datetime
###########################################
