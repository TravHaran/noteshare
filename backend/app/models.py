from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, SmallInteger, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship, backref

followers = Table(
    'followers', Base.metadata,
    Column('user_id', Integer,
        ForeignKey('users.id'), primary_key=True),
    Column('follower_id', Integer,
        ForeignKey('users.id'), primary_key=True),
    # Column('created_at', TIMESTAMP(timezone=True), 
    #     nullable=False, server_default=text('now()'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationships
    library = relationship("Library", backref="user")
    book = relationship("Book", backref="user")
    book_vote = relationship("BookVote", backref="user")
    comment = relationship("Comment", backref="user")
    comment_vote = relationship("CommentVote", backref="user")
    notification = relationship("Notification", backref="user")

    # librarian_patron_invite = relationship("PatronInvite", foreign_keys='PatronInvite.librarian_id', back_populates="librarian_patron_invite")
    # invitee_patron_invite = relationship("PatronInvite", foreign_keys='PatronInvite.invitee_id', back_populates="invitee_patron_invite")

    # user_patron_request = relationship("PatronRequest", foreign_keys='PatronRequest.user_id', back_populates="user_patron_request")
    # librarian_patron_request = relationship("PatronRequest", foreign_keys='PatronRequest.librarian_id', back_populates="librarian_patron_request")
    
    patron = relationship("Patron", backref="user")

    followers = relationship(
        'User', secondary=followers, cascade='all', lazy='dynamic',
        primaryjoin=followers.c.user_id == id,
        secondaryjoin=followers.c.follower_id == id)
    # following = relationship(
    #     "User", 
    #     secondary = "user_following",
    #     primaryjoin="User.id==user_following.c.user_id",
    #     secondaryjoin="User.id==user_following.c.follwing_id",
    #     backref="followers"
    # )

# user_following = Table(
#     "user_following",
#     Base.metadata,
#     Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
#     Column("following_id", Integer, ForeignKey("users.id"), primary_key=True)
# )

class Library(Base):
    __tablename__ = "libraries"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    public = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    book = relationship("Book", backref="libraries")
    patron_invite = relationship("PatronInvite", backref="libraries")
    patron_request = relationship("PatronRequest", backref="libraries")
    patron = relationship("Patron", backref="libraries")

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    file = Column(String, nullable=False)
    page_count = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    tag = relationship("Tag", secondary="book_tag_map", backref="books")
    book_vote = relationship("BookVote", backref="books")
    comment = relationship("Comment", backref="books")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship

book_tag_map = Table(
    "book_tag_map",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class BookVote(Base):
    __tablename__ = "book_votes"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    dir = Column(SmallInteger, nullable=False)
    __table_args__ = (CheckConstraint(dir.in_([-1, 0, 1])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    comment_vote = relationship("CommentVote", backref="comments")

class CommentVote(Base):
    __tablename__ = "comment_votes"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), nullable=False)
    dir = Column(SmallInteger, nullable=False)
    __table_args__ = (CheckConstraint(dir.in_([-1, 0, 1])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship

class Patron(Base):
    __tablename__ = "patrons"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    admin_level = Column(String, nullable=False)
    __table_args__ = (CheckConstraint(admin_level.in_(['librarian', 'author', 'reader'])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship

class PatronInvite(Base):
    __tablename__ = "patron_invites"
    id = Column(Integer, primary_key=True, nullable=False)
    inviter_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    invitee_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    admin_level = Column(String, nullable=False)
    __table_args__ = (CheckConstraint(admin_level.in_(['author', 'reader'])),)
    approved = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    inviter = relationship("User", foreign_keys=[inviter_id]) 
    invitee = relationship("User", foreign_keys=[invitee_id]) 
    # librarian_patron_invite = relationship("User", backref=backref("users", uselist=False), foreign_keys=[inviter_id])
    # invitee_patron_invite = relationship("User", backref=backref("users", uselist=False), foreign_keys=[invitee_id])

class PatronRequest(Base):
    __tablename__ = "patron_requests"
    id = Column(Integer, primary_key=True, nullable=False)
    requester_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    requestee_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    admin_level = Column(String, nullable=False)
    __table_args__ = (CheckConstraint(admin_level.in_(['author', 'reader'])),)
    approved = Column(Boolean, nullable=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    requester = relationship("User", foreign_keys=[requester_id]) 
    requestee = relationship("User", foreign_keys=[requestee_id]) 
    # user_patron_request = relationship("User", backref=backref("users", uselist=False), foreign_keys=[requester_id])
    # librarian_patron_request = relationship("User", backref=backref("users", uselist=False), foreign_keys=[requestee_id])

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    




