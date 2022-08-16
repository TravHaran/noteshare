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
    created_at: datetime
    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str
###########################################

############## Authorization Token Schemas ##############
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None
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
    owner_id: int
    owner: UserOut
    authors: int
    readers: int
    created_at: datetime
    class Config:
        orm_mode = True

class LibraryOut(BaseModel):
    Library: Library
###########################################

############## Book Schemas ##############
class BookBase(BaseModel):
    title: str
    description: Optional[str] = None
    content: str

class BookCreate(BookBase):
    pass

class Book(BookBase):
    id: int
    owner_id: int
    owner: UserOut
    likes: int
    dislikes: int
    comments: int
    created_at: datetime
    class Config:
        orm_mode = True

class BookOut(BaseModel):
    Book: Book
###########################################

############## PatronRequest Schemas ##############
class PatronRequestBase(BaseModel):
    library_id: int
    admin_level = str
    @validator('admin_level', check_fields=False)
    def verify_admin_level(cls, v):
        options = ['author', 'reader']
        if v not in options:
            raise ValueError(f'invalid admin level, please select from valid options: {options}')

class PatronRequestCreate(PatronRequestBase):
    pass

class PatronRequest(PatronRequestBase):
    user_id: int
    user: UserOut
    class Config:
        orm_mode = True

class PatronRequestOut(BaseModel):
    Request: PatronRequest

class GetPatrons(BaseModel):
    library_id: int

class Patron(BaseModel):
    user_id: int
    email: EmailStr
    username: str
    admin_level = str
    @validator('admin_level', check_fields=False)
    def validate_admin_level(cls, value):
        options = ['librarian', 'author', 'reader']
        if value not in options:
            raise ValueError(f'invalid admin level, please select from valid options: {options}')

class GetPatronsOut(BaseModel):
    Patron: Patron
###########################################

############## Comment Schemas ##############   
class CommentBase(BaseModel):
    book_id: int
    content: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
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

############## Follower Schemas ##############
class FollowUser(BaseModel):
    user_id: int
    dir: bool

class Follower(BaseModel):
    user_id: int
    username: str
    email: EmailStr
    class Config:
        orm_mode = True

class MyFollowerOut(BaseModel):
    Follower: Follower

class MyFollowingOut(BaseModel):
    Follower: Follower
###########################################

############## Notification Schemas ##############
class NotificationsOut(BaseModel):
    notification: str
    created_at: datetime
###########################################
