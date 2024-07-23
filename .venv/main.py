from fastapi import FastAPI, Request, Form, HTTPException, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from models import *
from crud import *
from typing import List

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Создаем базу данных и таблицы
create_db_and_tables()


@app.get("/support", response_class=HTMLResponse)
async def support(request: Request):
    return templates.TemplateResponse("support.html", {"request": request})

@app.get("/privacy-policy", response_class=HTMLResponse)
async def privacy_policy(request: Request):
    return templates.TemplateResponse("privacy_policy.html", {"request": request})

@app.get("/about-us", response_class=HTMLResponse)
async def about_us(request: Request):
    return templates.TemplateResponse("about_us.html", {"request": request})


@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/register")
async def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    address: str = Form(None)
):
    user = User(first_name=first_name, last_name=last_name, email=email, password=password, address=address)
    created_user = create_user(user)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/login")
async def login(
    request: Request,
    email: str = Form(...),
    password: str = Form(...)
):
    user = get_user_by_email(email)
    if user and user.password == password:
        response = RedirectResponse(url=f"/profile/{user.id}", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="user_id", value=str(user.id))  # сохраняем user_id в cookie
        return response
    return templates.TemplateResponse("index.html", {"request": request, "error": "Invalid credentials"})

@app.get("/profile/{user_id}", response_class=HTMLResponse)
async def view_profile(request: Request, user_id: int):
    user = get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    books = get_books_by_owner_id(user_id)
    exchanges = get_exchanges_by_owner_id(user_id)

    return templates.TemplateResponse("profile.html", {"request": request, "user": user, "books": books, "exchanges": exchanges})

@app.get("/login", response_class=HTMLResponse)
async def login_form(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_form(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/profile/{user_id}/add_book")
async def add_book(
    user_id: int,
    title: str = Form(...),
    author: str = Form(...),
    genre: str = Form(...),
    year: int = Form(...),
    condition: str = Form(...)
):
    book = Book(title=title, author=author, genre=genre, year=year, condition=condition, owner_id=user_id)
    created_book = create_book(book)
    return RedirectResponse(url=f"/profile/{user_id}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/profile/{user_id}/search_books")
async def search_books(request: Request, user_id: int, query: str = Form(...)):
    books = search_books_by_title_or_author(query)
    users_with_books = []
    for book in books:
        users_with_books.extend(get_users_with_book(book.id))
    return templates.TemplateResponse("search_results.html", {"request": request, "books": books, "users_with_books": users_with_books})

@app.post("/request_book")
async def request_book(request: Request, book_id: int = Form(...), user_id: int = Form(...)):
    exchange = Exchange(book_to_send_id=book_id, requester_id=user_id)
    create_exchange(exchange)
    return RedirectResponse(url=f"/profile/{user_id}", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/accept_exchange")
async def accept_exchange(request: Request, exchange_id: int = Form(...)):
    exchange = get_exchange_by_id(exchange_id)
    if exchange:
        exchange.status = "accepted"
        update_exchange(exchange)
        return RedirectResponse(url=f"/profile/{exchange.requester_id}", status_code=status.HTTP_303_SEE_OTHER)
    return HTTPException(status_code=404, detail="Exchange not found")

@app.post("/decline_exchange")
async def decline_exchange(request: Request, exchange_id: int = Form(...)):
    exchange = get_exchange_by_id(exchange_id)
    if exchange:
        exchange.status = "declined"
        update_exchange(exchange)
        return RedirectResponse(url=f"/profile/{exchange.requester_id}", status_code=status.HTTP_303_SEE_OTHER)
    return HTTPException(status_code=404, detail="Exchange not found")
