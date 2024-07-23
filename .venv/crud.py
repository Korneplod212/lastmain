from sqlmodel import SQLModel, create_engine, Session, select
from models import User, Book, Exchange
from sqlalchemy.orm import joinedload

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

def get_session():
    return Session(engine)

def create_user(user: User):
    with get_session() as session:
        session.add(user)
        session.commit()
        session.refresh(user)
        return user

def get_user_by_id(user_id: int):
    with get_session() as session:
        statement = select(User).where(User.id == user_id)
        return session.exec(statement).first()

def create_book(book: Book):
    with get_session() as session:
        session.add(book)
        session.commit()
        session.refresh(book)
        return book

def get_books_by_owner_id(owner_id: int):
    with get_session() as session:
        books = session.exec(select(Book).where(Book.owner_id == owner_id)).all()
        return books

def get_books():
    with get_session() as session:
        statement = select(Book)
        return session.exec(statement).all()

def search_books_by_title_or_author(query: str):
    with get_session() as session:
        statement = select(Book).where((Book.title.contains(query)) | (Book.author.contains(query)))
        return session.exec(statement).all()

def get_users_with_book(book_id: int):
    with get_session() as session:
        statement = select(User).join(Book, Book.owner_id == User.id).where(Book.id == book_id)
        return session.exec(statement).all()

def get_user_by_email(email: str):
    with get_session() as session:
        statement = select(User).where(User.email == email)
        return session.exec(statement).first()

def create_exchange(exchange: Exchange):
    with get_session() as session:
        session.add(exchange)
        session.commit()
        session.refresh(exchange)
        return exchange

def get_exchanges(user_id: int):
    with get_session() as session:
        statement = select(Exchange).where(Exchange.requester_id == user_id)
        return session.exec(statement).all()

def get_exchange_by_id(exchange_id: int):
    with get_session() as session:
        statement = select(Exchange).where(Exchange.id == exchange_id)
        return session.exec(statement).first()

def update_exchange(exchange: Exchange):
    with get_session() as session:
        session.add(exchange)
        session.commit()
        session.refresh(exchange)
        return exchange

def get_exchanges_by_owner_id(owner_id: int):
    with get_session() as session:
        statement = select(Exchange).options(joinedload(Exchange.book_to_send)).join(Book, Exchange.book_to_send_id == Book.id).where(Book.owner_id == owner_id)
        return session.exec(statement).all()
