from fastapi import APIRouter, Query, HTTPException
from models.book import BookModel
from schemas.book import BookCreate, BookUpdate

router = APIRouter(prefix="/books", tags=["Books"])

global_book_id: int = 0
books_db: list[BookModel] = []


@router.post("/", response_model=BookModel)
async def create_book(book_data: BookCreate):
    global global_book_id, books_db

    book_db = BookModel(id= global_book_id, **book_data.dict())

    global_book_id += 1

    books_db.append(book_db)
    return book_db


@router.get("/", response_model=list[BookModel])
async def get_all_books(author: str = Query(None), year: int = Query(None), tags: str = Query(None)):


    rep: list[BookModel] = []
    for book in books_db:

        if author is not None and book.author != author:
            continue
        if year is not None and book.year != year:
            continue
        if tags is not None:
            continue_flag = False
            for tag in tags.split(","):
                if tag not in book.tags:
                    continue_flag = True
            if continue_flag:
                continue

        rep.append(book)
    return rep


@router.get("/{book_id}", response_model=BookModel)
async def get_book(book_id: int):
    for book in books_db:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@router.patch("/update/{book_id}", response_model=BookModel)
async def update_book(book_id: int, book_data: BookUpdate):
    global books_db

    for index in range(len(books_db)):
        book_db = books_db[index]

        if book_db.id != book_id:
            continue

        updated_book = book_db.copy(update=book_data.dict(exclude_unset=True))
        books_db[index] = updated_book
        return updated_book
    raise HTTPException(status_code=404, detail="Book not found")

@router.delete("/{book_id}", response_model=BookModel)
async def delete_book(book_id: int):
    global books_db
    for index in range(len(books_db)):
        book_db = books_db[index]
        if book_db.id != book_id:
            continue

        books_db.pop(index)
        return {"message": "Book deleted"}
    raise HTTPException(status_code=404, detail="Book not found")