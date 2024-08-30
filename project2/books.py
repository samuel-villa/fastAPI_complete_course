"""
DATA VALIDATION with Pydantic

Pydantic v1 vs Pydantic v2

FastAPI is now compatible with both Pydantic v1 and Pydantic v2.
Based on how new the version of FastAPI you are using, there could be small method name changes.

The three biggest are:
* .dict() function is now renamed to .model_dump()
* schema_extra function within a Config class is now renamed to json_schema_extra
* Optional variables need a =None example: id: Optional[int] = None
"""

from typing import Optional
from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from starlette import status


app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int
    published_date: int

    def __init__(self, id, title, author, description, rating, published_date):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating
        self.published_date = published_date


class BookRequest(BaseModel):
    id: Optional[int] = Field(description='ID is not needed on create', default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)  # 1 to 5
    published_date: int = Field(gt=1999, lt=2031)

    # add custom Swagger example
    model_config = {
        "json_schema_extra": {
            "example": {
                "title": "A new book",
                "author": "Samuel C.",
                "description": "A great book",
                "rating": 5,
                "published_date": 2029,
            }
        }
    }


BOOKS = [
    Book(1, 'Computer Science Pro', 'codingwithroby', 'A very nice book', 5, 2015),
    Book(2, 'Book 2', 'author 2', 'desc 2', 5, 2016),
    Book(3, 'Book 3', 'author 3', 'desc 3', 4, 1999),
    Book(4, 'Book 4', 'author 4', 'desc 4', 5, 2000),
    Book(5, 'Book 5', 'author 5', 'desc 5', 2, 2024),
]


# We explicitly give a successful response with starlette.status
@app.get("/books", status_code=status.HTTP_200_OK)
def get_books():
    return BOOKS


# PATH Validation with Path()
@app.get("/books/{book_id}")
def get_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Item not found")
        

# QUERY Validation with Query()
@app.get("/books/", status_code=status.HTTP_200_OK)
def get_book_by_rating(book_rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == book_rating:
            books_to_return.append(book)
    return books_to_return


# QUERY Validation with Query()
@app.get("/books/publish/", status_code=status.HTTP_200_OK)
def get_book_by_published_date(published_date: int = Query(gt=1999, lt=2031)):
    books_to_return = []
    for book in BOOKS: 
        if book.published_date == published_date:
            books_to_return.append(book)
    return books_to_return


@app.post("/create_book", status_code=status.HTTP_201_CREATED)
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))


def find_book_id(book: Book):
    """update new book id
    """
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/update_book", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book: BookRequest):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book.id:
            BOOKS[i] = book
            book_changed = True
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not founf")


# PATH Validation with Path()
@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_changed = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            BOOKS.pop(i)
            book_changed = True
            break
    if not book_changed:
        raise HTTPException(status_code=404, detail="Item not founf")

