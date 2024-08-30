"""
* Interaction with SQLite DB
* Routing
* Authentication
* Hashed Password
"""
from fastapi import FastAPI
import models
from database import engine
from routers import auth, todos, admin, users


app = FastAPI()

models.Base.metadata.create_all(bind=engine)  # creates the DB file (IF DOES NOT EXIST)

app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
