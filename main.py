from typing import Any
from fastapi import FastAPI
from enum import Enum

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/")
async def post_root():
    return {"message": "Hello from Post route"}


@app.put("/")
async def put_route():
    return {"message": "Hello from Put route"}


@app.get("/users")
async def get_users():
    return {"message": "List all users"}


@app.get("/users/{user_id}")
async def get_user(user_id: int):
    return {"message": f"Get user with id {user_id}"}


class FoodEnum(str, Enum):
    fruits = "fruits"
    vegetables = "vegetables"
    dairy = "dairy"


@app.get("/foods/{food_name}")
async def get_food(food_name: FoodEnum):
    if food_name == FoodEnum.vegetables:
        return {"food name": food_name, "message": "Healthy Veggies"}
    if food_name == FoodEnum.fruits:
        return {"food name": food_name, "message": "Healthy Fruits"}
    if food_name == FoodEnum.dairy:
        return {"food name": food_name, "message": "Milk Products"}


items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get("/items")
async def get_items(skip: int = 0, limit: int = 10):
    return items_db[skip : skip + limit]


# FastAPI recognizes path params and query params (since they are primitive types)
# has optional query parameters --> 'q' which can be None + short which is bool (that adds description to item dict when T)
# old way to declare optional query params --> Optional[str] = None
@app.get("/items/{item_id}")
async def get_item(
    item_id: str, query_param: str, q: str | None = None, short: bool = False
):
    item = {"item_id": item_id, "query_param": query_param}
    if q:
        item.update({"q": q})
    if not short:
        item.update({"description": "This a description for the queried item"})
    return item  # FastAPI will convert dict and return response as JSON object


@app.get("/users/{user_id}/items/{items_id}")
async def get_user_item(
    user_id: int, items_id: int, q: str | None = None, short: bool = False
):
    item: dict[str, Any] = {"item_id": items_id, "owner_id": user_id}
    if q:
        item.update({"q": q})
    if not short:
        item.update(
            {
                "description": "This is a description for the queried item that belongs to the user"
            }
        )
    return item
