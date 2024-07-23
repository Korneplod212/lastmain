from sqlmodel import Field, SQLModel, create_engine, Session, Relationship
from typing import Optional, List

class Book(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str
    author: str
    genre: str
    year: int
    condition: str
    rating: Optional[float] = None
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: "User" = Relationship(back_populates="books")
    exchanges: List["Exchange"] = Relationship(back_populates="book_to_send")

class Exchange(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    book_to_send_id: Optional[int] = Field(default=None, foreign_key="book.id")
    book_to_send: "Book" = Relationship(back_populates="exchanges")
    requester_id: Optional[int] = Field(default=None, foreign_key="user.id")
    requester: "User" = Relationship(back_populates="exchanges")
    status: str = Field(default="pending")

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    first_name: str
    last_name: str
    email: str = Field(unique=True)
    password: str
    address: Optional[str] = None
    books: List["Book"] = Relationship(back_populates="owner")
    exchanges: List["Exchange"] = Relationship(back_populates="requester")

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    return Session(engine)
