from .database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, CheckConstraint, SmallInteger, Table
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship, backref

class Library(Base):
    __tablename__ = "libraries"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    public = Column(Boolean, server_default='True', nullable=False)
    banner = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    # Relationship
    users = relationship("User", back_populates="libraries")
    books = relationship("Book", back_populates="libraries")
    patron_invite = relationship("PatronInvite", back_populates="libraries")
    patron_request = relationship("PatronRequest", back_populates="libraries")
    patrons = relationship("User", secondary="patrons", back_populates="libraries")

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
    libraries = relationship("Library", back_populates="users")
    books = relationship("Book", back_populates="users")
    comments = relationship("Comment", back_populates="users")
    book_votes = relationship("BookVote", back_populates="users")
    comment_votes = relationship("CommentVote", back_populates="users")
    notifications = relationship("Notification", back_populates="users")
    patrons = relationship("Library", secondary="patrons", back_populates="users", overlaps="patrons")
    downloads = relationship("Download", back_populates="users")
    # patron = relationship("Patron", back_populates="users")
    # patron_invite = relationship("PatronInvite", back_populates="users")
    # patron_request = relationship("PatronRequest", back_populates="users")

    # librarian_patron_invite = relationship("PatronInvite", foreign_keys='PatronInvite.librarian_id', back_populates="librarian_patron_invite")
    # invitee_patron_invite = relationship("PatronInvite", foreign_keys='PatronInvite.invitee_id', back_populates="invitee_patron_invite")

    # user_patron_request = relationship("PatronRequest", foreign_keys='PatronRequest.user_id', back_populates="user_patron_request")
    # librarian_patron_request = relationship("PatronRequest", foreign_keys='PatronRequest.librarian_id', back_populates="librarian_patron_request")

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

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    file = Column(String, nullable=False)
    thumbnail = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    tag = relationship("Tag", secondary="book_tag_map", back_populates="books")
    book_votes = relationship("BookVote", back_populates="books")
    downloads = relationship("Download", back_populates="books")
    comments = relationship("Comment", back_populates="books")
    users = relationship("User", back_populates="books")
    libraries = relationship("Library", back_populates="books")
    tags = relationship(
        "Tag",
        secondary="book_tag_map",
        back_populates="books",
        overlaps="tag"
    )

class Download(Base):
    __tablename__ = "downloads"
    id = Column(Integer, primary_key=True, nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    books = relationship("Book", back_populates="downloads")
    users = relationship("User", back_populates="downloads")

class Tag(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    books = relationship(
        "Book",
        secondary="book_tag_map",
        back_populates="tags"
    )

book_tag_map = Table(
    "book_tag_map",
    Base.metadata,
    Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
)

class BookVote(Base):
    __tablename__ = "book_votes"
    # id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    dir = Column(Integer, nullable=False)
    __table_args__ = (CheckConstraint(dir.in_([-1, 0, 1])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    books = relationship("Book", back_populates="book_votes")
    users = relationship("User", back_populates="book_votes")

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    # Relationship
    comment_votes = relationship("CommentVote", back_populates="comments")
    users = relationship("User", back_populates="comments")
    books = relationship("Book", back_populates="comments")

class CommentVote(Base):
    __tablename__ = "comment_votes"
    # id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)
    dir = Column(SmallInteger, nullable=False)
    __table_args__ = (CheckConstraint(dir.in_([-1, 0, 1])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    comments = relationship("Comment", back_populates="comment_votes")
    users = relationship("User", back_populates="comment_votes")

# book_tag_map = Table(
#     "book_tag_map",
#     Base.metadata,
#     Column("book_id", ForeignKey("books.id", ondelete="CASCADE"), primary_key=True),
#     Column("tag_id", ForeignKey("tags.id", ondelete="CASCADE"), primary_key=True)
# )

class Patron(Base):
    __tablename__ = "patrons"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), primary_key=True)
    admin_level = Column(String, nullable=False)
    __table_args__ = (CheckConstraint(admin_level.in_(['librarian', 'author', 'reader'])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    # libraries = relationship("Library", back_populates="patrons")
    # users = relationship("User", back_populates="patrons")

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
    libraries = relationship("Library", foreign_keys=[library_id])
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
    libraries = relationship("Library", foreign_keys=[library_id])
    # user_patron_request = relationship("User", backref=backref("users", uselist=False), foreign_keys=[requester_id])
    # librarian_patron_request = relationship("User", backref=backref("users", uselist=False), foreign_keys=[requestee_id])

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    # Relationship
    users = relationship("User", back_populates="notifications")
    




