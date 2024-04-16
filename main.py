from re import L
from typing import Any, List
from fastapi import Body, FastAPI, Path, Query
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, HttpUrl

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


# @app.post("/")
# async def post_root():
#     return {"message": "Hello from Post route"}


# @app.put("/")
# async def put_route():
#     return {"message": "Hello from Put route"}


# @app.get("/users")
# async def get_users():
#     return {"message": "List all users"}


# # USING PATH PARAMS
# @app.get("/users/{user_id}")
# async def get_user(user_id: int):
#     return {"message": f"Get user with id {user_id}"}


# class FoodEnum(str, Enum):
#     fruits = "fruits"
#     vegetables = "vegetables"
#     dairy = "dairy"


# @app.get("/foods/{food_name}")
# async def get_food(food_name: FoodEnum):
#     if food_name == FoodEnum.vegetables:
#         return {"food name": food_name, "message": "Healthy Veggies"}
#     if food_name == FoodEnum.fruits:
#         return {"food name": food_name, "message": "Healthy Fruits"}
#     if food_name == FoodEnum.dairy:
#         return {"food name": food_name, "message": "Milk Products"}


# # USING QUERY PARAMS
# items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


# @app.get("/items")
# async def get_items(skip: int = 0, limit: int = 10):
#     return items_db[skip : skip + limit]


# # FastAPI recognizes path params (explicitly declared in route definition) and query params (primitive types)
# # has optional query parameters --> 'q' which can be None + short which is bool (that adds description to item dict when T)
# # old way to declare optional query params --> Optional[str] = None
# @app.get("/items/{item_id}")
# async def get_item(
#     item_id: str, query_param: str, q: str | None = None, short: bool = False
# ):
#     item = {"item_id": item_id, "query_param": query_param}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update({"description": "This a description for the queried item"})
#     return item  # FastAPI will convert dict and return response as JSON object


# @app.get("/users/{user_id}/items/{items_id}")
# async def get_user_item(
#     user_id: int, items_id: int, q: str | None = None, short: bool = False
# ):
#     item: dict[str, Any] = {"item_id": items_id, "owner_id": user_id}
#     if q:
#         item.update({"q": q})
#     if not short:
#         item.update(
#             {
#                 "description": "This is a description for the queried item that belongs to the user"
#             }
#         )
#     return item


# # POST/PUT - USING REQUEST BODY
# class Item(BaseModel):
#     name: str
#     description: str | None = None
#     price: float
#     tax: float | None = None


# @app.post("/items")
# async def create_item(item: Item):
#     item_dict = item.model_dump()
#     if item.tax:
#         price_with_tax = item.price + item.tax
#         item_dict.update({"price_with_tax": price_with_tax})
#     return item_dict


# @app.put("/items/{item_id}")
# async def update_item(item_id: int, item: Item, q: str | None = None):
#     result = {"item_id": item_id, **item.model_dump()}
#     if q:
#         result.update({"q": q})
#     return result


# # QUERY PARAMS AND STRING VALIDATION
# @app.get("/items")
# async def read_items(
#     q: str | None = Query(
#         None, min_length=3, max_length=10, title="Sample query string"
#     ),
#     # !!remove | None and add ... to make it required (also has no default value now - you can set default instead)
#     # !!use list[str] to specify that it should be a list of strings i.e multiple query params
#     # alias is used since python not able to allow certain chars/symbols in name (in this example '-') [this changes how query is displayed in the URL]
#     # async def read_items(
#     #     q: list[str] = Query(
#     #         ..., min_length=3, max_length=10, title="Sample query string"
#     #     ),
#     description="This is a sample query string.",
#     alias="items-query",
# ):
#     results: dict[str, Any] = {"items": [{"items_id": "Foo"}, {"items_id": "Bar"}]}
#     if q:
#         results.update({"q": q})
#     return results


# # setting include_in_schema=False will exclude the param from the generated OpenAPI schema (docs)
# @app.get("/items_hidden")
# async def hidden_query_route(
#     hidden_query: str | None = Query(None, include_in_schema=False)
# ):
#     if hidden_query:
#         return {"hidden query": hidden_query}
#     return {"message": "Hidden query param not provided"}


# # PATH PARAMS AND NUMERIC VALIDATION
# @app.get("/items_validation/{item_id}")
# # see notes for using '*'
# async def read_items_validation(
#     *,
#     item_id: int = Path(..., title="The ID of the items to get", gt=0, le=100),
#     q: str = "hello",
#     size: float = Query(..., gt=0, lt=7.75),
# ):
#     results = {"item_id": item_id, "size": size}
#     if q:
#         results.update({"q": q})
#     return results


# 1. MULTIPLE PARAMS (dict) in BODY - INCLUDE QUERY AND PATH PARAMS IN REQUEST BODY
# 2. ADDING FIELDS/DESCRIPTIVE DATA TO THE REQUEST BODY
class Item(BaseModel):
    name: str
    description: str | None = Field(
        default=None, title="Description of the item", max_length=300
    )
    price: float = Field(gt=0, description="The Price must be greater than zero")
    tax: float | None = None


class User(BaseModel):
    username: str
    fullname: str | None = None


@app.put("/items/{item_id}")
async def update_item_v2(
    *,
    item_id: int = Path(..., title="The ID of the item to update", ge=0, le=150),
    q: str | None = None,
    item: Item | None = None,
    user: User,
    # use item: Item = Body(..., embed=True) to embed item as the key with the dict being the value in the body
    importance: int = Body(
        ...,
    )  # eg if it is just a single value not a nested dict
):
    results: dict[str, Any] = {"item_id": item_id}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": User})
    if importance:
        results.update({"importance": importance})
    return results


# 1.NESTED MODELS within Pydantic model attribute types
# 2.DECLARE REQUEST EXAMPLE DATA that app can receive (multiple methods to do this). Able to pass multiple examples
## 2(a) Extra JSON schema data in Pydanitc Models (declare examples using model_config: dict that will be added to auto-generated JSON schema API docs).
## 2(b) Using Field(0) you can declare additional examples
## 2(c) Passing eg. Body/Path/Query/Header/Cookie(examples=[{use keys from schema and declare examples}])
##2(d) OpenAPI-specific exmaples - focus on path operation not JSON Schema. examples: dict and goes in path operation directly. Passing eg. Body/Path/Query/Header/Cookie(openapi_examples={use keys from schema and declare examples})
class Image(BaseModel):
    url: HttpUrl
    name: str


class Item_v2(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = Field(examples=[3.2, 0.5])
    # tags: List[str] = [] <= 3.8 Python and syntax
    tags: list[str] = []  # >= 3.9
    # tags: set[str] = set() for unique values
    image: list[Image] | None = None
    # 2(a) Can also be used to extend schema with your own custom data https://docs.pydantic.dev/latest/api/config/#pydantic.config.ConfigDict.str_strip_whitespace
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Foo",
                    "description": "A very nice item",
                    "price": 35.4,
                    "tax": 3.2,
                }
            ]
        }
    }


class Offer(BaseModel):
    name: str
    description: str | None = None
    price: float
    items: list[Item_v2]


@app.put("/items_v2/{item_id}")
async def update_item_v3(item_id: int, item: Item_v2):
    results = {"item_id": item_id, "item": item}
    return results


@app.post("/offers")
async def create_offer(offer: Offer = Body(..., embed=True)):
    return offer


# Body function to indicate that the offer data should come from the request body.
# The embed=True argument tells FastAPI to expect the Offer data to be under the offer key in the request body.
@app.post("/images/multiple")
async def create_multiple_images(images: list[Image]):
    return images


# Note JSON only supports str as keys, but Pydantic auto converts data
@app.post("/blah")
async def create_some_blahs(blahs: dict[int, float]):
    return blahs


# RESPONSE MODEL & RETURN TYPE -
# # 1. declare type used for repsonse by adding {async def create_item(item: Item) -> TYPE eg. Item} after the route definition
# eg. create an output model specifically for response data
# # FastAPI will use this return type to Validate the response data and generate the OpenAPI JSON schema + IMP filter & limit output data to only defined/decalred types, fields which is important for security.
# # 2. 'response_model' parameter in route decorator to specify the response model eg. @app.post("/items/", response_model=Item)
# # if both are defined then 'response_model' takes priority over return type ->


# example
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: str | None = None


# use to validate request body
class UserInDB(UserBase):
    password: str


# use to format the response
class UserOut(UserBase):
    pass


@app.post("/user_in_out_test", response_model=UserOut)
async def create_user_in_out(user: UserInDB):
    return user


class Item_v2_res(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None
    tags: list[str] = []
    image: list[Image] | None = None


@app.get("/items_v2/{item_id}", response_model=Item_v2_res)
async def read_item_v2_with_response_model(item_id: int):
    return {
        "name": "Foo",
        "description": "GET route using response_model to validate response data",
        "price": 35.4,
        "tax": 3.2,
        "tags": ["tag1", "tag2"],
        "image": [
            {"url": "http://image1.jpg", "name": "image1"},
            {"url": "http://image2.jpg", "name": "image2"},
        ],
    }
