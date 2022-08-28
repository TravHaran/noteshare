from pydantic import BaseModel, EmailStr

from datetime import datetime
from typing import Optional, List

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
    class Config:
        orm_mode = True

class BookVote(VoteBase):
    book_id: int

class BookVoteOut(BaseModel):
    vote: BookVote
    
    
class CommentVote(VoteBase):
    comment_id: int

class CommentVoteOut(BaseModel):
    vote: CommentVote
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
    class Config:
        orm_mode = True

class CommentOut(BaseModel):
    Comment: Comment
    votes: CommentVote
    user: UserOut
    class Config:
        orm_mode = True
###########################################

############## Chat Schemas ##############   
class ChatBase(BaseModel):
    library_id: int
    content: str

class ChatCreate(ChatBase):
    pass

class Comment(ChatBase):
    id: int
    user_id: int
    created_at: datetime
    class Config:
        orm_mode = True

# class CommentOut(BaseModel):
#     Comment: Comment
#     votes: CommentVote
#     user: UserOut
#     class Config:
#         orm_mode = True
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
    ########
    # votes: VoteBook
    # tags: TagOut
    # library: Library
    # owner: UserOut
    ########
    class Config:
        orm_mode = True

class LibraryBase(BaseModel):
    title: str
    description: str
    public: bool = True

class LibraryCreate(LibraryBase):
    pass

class Library(LibraryBase):
    id: int
    banner: str
    created_at: datetime
    ########
    owner_id: int
    owner: UserOut
    ########
    class Config:
        orm_mode = True

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
    # book: Book
    class Config:
        orm_mode = True

class TagDelete(BaseModel):
    tag_ids: list[int]
###########################################

class BookOut(BaseModel):
    book: Book
    owner: UserOut
    library: Library
    likes: int
    dislikes: int
    tags: TagOut
    comments: CommentOut
    class Config:
        orm_mode = True
###########################################

############## Library Schemas ##############

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

############## PatronRequest Schemas ##############
class PatronRequestBase(BaseModel):
    library_id: int
    admin_level: str

class PatronRequestCreate(PatronRequestBase):
    pass

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
    library_id: int
    patron_id: int
    admin_level: str

class PatronInviteCreate(PatronInviteBase):
    # this action can only be performed by librarian of library to which aptron is being invited to
    pass
    
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
class PatronBase(BaseModel):
    library_id: int
    user_id: int
    admin_level: str

class PatronCreate(PatronBase):
    pass

class Patron(PatronBase):
    id: int
    ########
    user: UserOut
    ########
    created_at: datetime
    class Config:
        orm_mode = True

class GetPatronsOut(BaseModel):
    Patron: Patron
    class Config:
        orm_mode = True
###########################################

############## Notification Schemas ##############
class Notifications(BaseModel):
    id: int
    message: str
    created_at: datetime
###########################################
