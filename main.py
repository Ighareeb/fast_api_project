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


@app.get("/users/{id}")
async def get_user(id: int):
    return {"message": f"Get user with id {id}"}


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
