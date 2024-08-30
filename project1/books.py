from fastapi import Body, FastAPI

app = FastAPI()


BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


### Assignment: Get all books by author using PATH or QUERY parameters ###

# @app.get("/books/by_author/{author}")
# def get_books_by_author_path(author: str):
#     books_to_return = []
#     for book in BOOKS:
#         if book.get('author').casefold() == author.casefold():
#             books_to_return.append(book)
#     return books_to_return


@app.get("/books/by_author/")
def get_books_by_author_query(author: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == author.casefold():
            books_to_return.append(book)
    return books_to_return

### End Assignment ###



@app.get("/books")
def get_books():
    return BOOKS


# DYNAMIC PATH parameter
@app.get("/books/{book_title}")
def get_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book


# QUERY parameter
@app.get("/books/")
def get_book_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('category').casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


# DYNAMIC PATH parameter + QUERY parameter
@app.get("/books/{book_author}/")
def get_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get('author').casefold() == book_author.casefold() and \
        book.get('category').casefold() == category.casefold():
            books_to_return.append(book)

    return books_to_return


@app.post("/books/create_book")
def create_book(new_book=Body()):
    BOOKS.append(new_book)


@app.put("/books/update_book")
def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == updated_book.get('title').casefold():
            BOOKS[i] = updated_book


@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        if BOOKS[i].get('title').casefold() == book_title.casefold():
            BOOKS.pop(i)
            break
