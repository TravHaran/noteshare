from database import Base
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, LargeBinary, CheckConstraint, SmallInteger
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    username = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Library(Base):
    __tablename__ = "libraries"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    public = Column(Boolean, server_default='True', nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), nullable=False)
    library = relationship("Library")
    content = Column(LargeBinary, nullable=False)
    page_count = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class VoteBook(Base):
    __tablename__ = "book_votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    owner = relationship("User")
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), primary_key=True)
    book = relationship("Book")
    dir = Column(SmallInteger, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Comment(Base):
    __tablename__ = "comments"
    id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    book_id = Column(Integer, ForeignKey("books.id", ondelete="CASCADE"), nullable=False)
    book = relationship("Book")
    content = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class VoteComment(Base):
    __tablename__ = "comment_votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    owner = relationship("User")
    comment_id = Column(Integer, ForeignKey("comments.id", ondelete="CASCADE"), primary_key=True)
    comment = relationship("Comment")
    dir = Column(SmallInteger, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Patron(Base):
    __tablename__ = "patrons"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    user = relationship("User")
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), primary_key=True)
    library = relationship("Library")
    admin_level = Column(String, nullable=False)
    __table_args__ = (CheckConstraint(admin_level.in_(['librarian', 'author', 'reader'])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class PatronRequest(Base):
    __tablename__ = "patron_requests"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    user = relationship("User")
    library_id = Column(Integer, ForeignKey("libraries.id", ondelete="CASCADE"), primary_key=True)
    library = relationship("Library")
    admin_level = Column(String, nullable=False)
    __table_args__ = (CheckConstraint(admin_level.in_(['author', 'reader'])),)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))

class Follower(Base):
    __tablename__ = "followers"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    follower_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

class Notification(Base):
    __tablename__ = "notifications"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    notification = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))




