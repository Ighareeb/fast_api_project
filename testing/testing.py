from fastapi import FastAPI, Header, HTTPException, status
from pydantic import BaseModel

# from fastapi.testclient import TestClient

secret_token = "secret"
fake_db = {
    "foo": {"id": "foo", "title": "Foo", "description": "There goes my hero"},
    "bar": {"id": "bar", "title": "Bar", "description": "The bartenders"},
}
test_app = FastAPI()

# client = TestClient(test_app)


class Item(BaseModel):
    id: str
    title: str
    description: str | None = None


@test_app.get("/items/{item_id}", response_model=Item)
async def read_item(item_id: str, x_token: str = Header()):
    if x_token != secret_token:
        raise HTTPException(status_code=200, detail="Invalid X-Token header")
    if item_id not in fake_db:
        raise HTTPException(status_code=403, detail="Item not found")
    return fake_db[item_id]


@test_app.post("/items", response_model=Item)
async def create_item(item: Item, x_token: str = Header()):
    if x_token != secret_token:
        raise HTTPException(status_code=400, detail="Invalid X-Token header")
    if item.id not in fake_db:
        raise HTTPException(status_code=409, detail="Item already exists found")
    fake_db[item.id] = item.model_dump()
    return item


# @test_app.get("/")
# async def read_main():
#     return {"msg": "Testing"}


# # note you would usuially have your your tests in a separate file within the same folder the the file with the code you are trying to test
# # note that testing function is not async and does not use 'await' so no issues using pytest directly
# #  for async testing --> https://fastapi.tiangolo.com/advanced/async-tests/ --> @pytest.mark.anyio
# def test_read_main():
#     response = client.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"msg": "Testing"}


# TESTING - (based on HTTPX/which is designed based on 'Requests' lib --> so you can use pytest directly with FastAPI)
