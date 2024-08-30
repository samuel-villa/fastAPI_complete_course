"""
This file containes reusable code used by test files
"""

from sqlalchemy import create_engine, text
from sqlalchemy.pool import StaticPool
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from fastapi.testclient import TestClient
import pytest
from ..models import Todos, Users
from ..routers.auth import bcrypt_context


# create a Testing SQLite DB
SQLALCHEMY_DATABASE_URL = "sqlite:///./project3_TodoApp_postgresql/testdb.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


# Override get_db() and get_current_user() in order to call
# the below override functions ONLY when we run the tests...
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


def override_get_current_user():
    return {"username": "samciutest", "id": 1, "role": "admin"}


client = TestClient(app)


@pytest.fixture
def test_todo():
    todo = Todos(
        title="Learn to code",
        description="everyday",
        priority=5,
        complete=False,
        owner_id=1,
        # 'id' will be 1
    )
    db = TestingSessionLocal()  # this will instantiate the test on the TEST DB
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todos;"))
        connection.commit()


@pytest.fixture
def test_user():
    user = Users(
        username="samciutest",
        email="samciutest@email.com",
        first_name="sam",
        last_name='test',
        hashed_password=bcrypt_context.hash('testpassword'),
        role='admin',
        phone_number='1111-111111'
    )
    db = TestingSessionLocal()  # this will instantiate the test on the TEST DB
    db.add(user)
    db.commit()

    # use it in test files
    yield user

    # once finished, delete the test user
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM users;"))
        connection.commit()
