from ..main import app
from ..routers.todos import get_db, get_current_user
from fastapi import status
from ..models import Todos
from .utils import *


app.dependency_overrides[get_db] = override_get_db
app.dependency_overrides[get_current_user] = override_get_current_user


def test_get_all_authenticated(test_todo):
    """
    This test will be using the object yielded above => see test_todo()
    """
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == [
        {
            "id": 1,
            "complete": False,
            "title": "Learn to code",
            "description": "everyday",
            "priority": 5,
            "owner_id": 1,
        }
    ]


# argument test_todo is called from a fixture located in utils.py
def test_get_one_authenticated(test_todo):
    """
    This test will be using the object yielded above => see test_todo()
    """
    response = client.get("/todo/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {
        "id": 1,
        "complete": False,
        "title": "Learn to code",
        "description": "everyday",
        "priority": 5,
        "owner_id": 1,
    }


def test_get_one_authenticated_not_found():
    response = client.get("/todo/999")  # id 999 doesn't exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_create_todo(test_todo):
    request_data = {
        "title": "new todo",
        "description": "new todo description",
        "priority": 5,
        "complete": False,
    }

    # we test if the status code is ok
    response = client.post("/todo/", json=request_data)
    assert response.status_code == 201

    # we test if the object is actually in the db
    db = TestingSessionLocal()
    # because there is another test before this one the 'id' now will be 2
    model = db.query(Todos).filter(Todos.id == 2).first()
    assert model.title == request_data.get("title")
    assert model.description == request_data.get("description")
    assert model.priority == request_data.get("priority")
    assert model.complete == request_data.get("complete")


def test_update_todo(test_todo):
    request_data = {
        "title": "title updated",  # new value here
        "description": "everyday",
        "priority": 5,
        "complete": False,
    }

    # we test if the status code is ok
    response = client.put("/todo/1", json=request_data)
    assert response.status_code == 204
    # we test if the object value from the db matches the new value
    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model.title == "title updated"


def test_update_todo_not_found(test_todo):
    request_data = {
        "title": "title updated",  # new value here
        "description": "everyday",
        "priority": 5,
        "complete": False,
    }

    # we test if the status code is ok
    response = client.put("/todo/999", json=request_data)
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}


def test_delete_todo(test_todo):
    response = client.delete("/todo/1")
    assert response.status_code == 204

    db = TestingSessionLocal()
    model = db.query(Todos).filter(Todos.id == 1).first()
    assert model is None


def test_delete_todo_not_found():
    response = client.delete("/todo/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}
