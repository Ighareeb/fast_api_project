from .testing import test_app
from fastapi.testclient import TestClient


client = TestClient(test_app)


def test_read_item():
    response = client.get("/item/foo", headers={"X-Token": "secret"})
    # assert response.status_code == 200
    assert response.json() == {
        "id": "foo",
        "title": "Foo",
        "description": "There goes my hero",
    }


def test_read_item_bad_token():
    response = client.get("/items/foo", headers={"X-Token": "wrong_token"})
    # assert response.status_code == 400
    assert response.json() == {"detail": "Invalid X-Token header"}


def test_read_item_nonexistant_item():
    response = client.get("/items/baz", headers={"X-Token": "secret"})
    # assert response.status_code == 400
    assert response.json() == {"detail": "Item not found"}


def test_create_item():
    response = client.post(
        "/items",
        headers={"X-Token": "secret"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Bar"},
    )
    # assert response.status_code == 200
    assert response.json() == {
        "id": "foobar",
        "title": "Foo Bar",
        "description": "The Foo Bar",
    }


def test_create_item_bad_token():
    response = client.post(
        "/items",
        headers={"X-Token": "wrong_token"},
        json={"id": "foobar", "title": "Foo Bar", "description": "The Foo Bar"},
    )
    # assert response.status_code == 400
    assert response.json() == "Invalid X-Token header"


def test_create_existing_item():
    response = client.post(
        "/items",
        headers={"X-Token": "secret"},
        json={
            "id": "foo",
            "title": "Foo already exists",
            "description": "test to see if post stops overwritting existing item",
        },
    )
    # assert response.status_code == 409
    assert response.json() == "Item already exists"
