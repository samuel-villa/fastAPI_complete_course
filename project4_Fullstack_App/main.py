"""
* Interaction with SQLite DB
* Routing
* Authentication
* Hashed Password
"""
from fastapi import FastAPI, Request, status
from .models import Base
from .database import engine
from .routers import auth, todos, admin, users
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse


app = FastAPI()

Base.metadata.create_all(bind=engine)  # creates the DB file (IF DOES NOT EXIST)

app.mount('/static', StaticFiles(directory='project4_Fullstack_App/static'), name='static')


@app.get('/')
def redirect_to_todos(request: Request):
    return RedirectResponse(url='/todos/todo-page', status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {'status': 'Healthy'}


app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
