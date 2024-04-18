from datetime import datetime
from re import L
from typing import Any, List, Union
from fastapi import (
    Body,
    FastAPI,
    File,
    HTTPException,
    Path,
    Query,
    UploadFile,
    status,
    Form,
)
from enum import Enum

from fastapi.encoders import jsonable_encoder
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
#     # !!use List[str] to specify that it should be a list of strings i.e multiple query params
#     # alias is used since python not able to allow certain chars/symbols in name (in this example '-') [this changes how query is displayed in the URL]
#     # async def read_items(
#     #     q: List[str] = Query(
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
    tags: List[str] = []  # <= 3.8 Python and syntax
    # tags: list[str] = []  # >= 3.9
    # tags: set[str] = set() for unique values
    # image: list[Image] | None = None
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
    items: List[Item_v2]


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
async def create_multiple_images(images: List[Image]):
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
    tags: List[str] = []
    image: List[Image] | None = None


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


# RESPONSE STATUS CODES - same as response_model - declare status_code in route decorator
##  use with (HTTPStatus from http) or (HTTPException OR status from fastapi)
## app.post('/items)', status_code=status.HTTP_201_CREATED)


# FORM DATA/FIELDS - use Form from fastapi to declare form data in route
## When you need to receive form fields instead of JSON, you can use Form. [pip install python-multipart]
##!IMP if you use Body() then you will receive the form data as (JSON) a dict with the form field names as keys and the form field values as values, if you use Form() you will receive the form data as the form field values directly.
## You can't declare both Form and Body params in the same route. ( since request will have body encoded with eg. application/x-www-form-urlencoded or multipart/form-data) instead of application/json
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}


# REQUEST FILES - using File() from fastapi to define files to upload
## !!since uploaded files sent as form data (need python-multipart)


# For small files, you can read the file into memory and return it as bytes using File
# when defining file as bytes, FastAPI will read the file into memory and return the file as bytes. If you want to save the file to disk, you can use UploadFile instead of bytes.
@app.post("/files")
# async def create_file(file: bytes | None = File()):
# async def create_file(file: bytes = File(...)): ##make file required
async def create_file(
    file: bytes = File(description="The file to upload", max_length=1000000)
):
    if file is None:
        return {"message": "No file provided"}
    else:
        return {"file_size": len(file)}


@app.post("/files")
# multiple file upload
async def create_multiple_files(
    files: List[bytes] = File(description="The file to upload", max_length=1000000)
):
    return {"file_sizes": [len(file) for file in files]}


# async def create_upload_files(files: List[UploadFile]):
# return {"filenames": [file.filename for file in files]}


# For larger files eg. images, videos.
# can use 'file' object methods to access attributes/K:V or use methods do CRUD operations on the file
# UploadFile has following attributes:  *filename = str with original file name, *content_type = str with file content type, *file = SpooledTemporaryFile (the actual python file you can pass around like an object),
# !Async methods: *write(data: str/bytes), *read(size: int -either bytes or chars in file), *readline(), *seek(offset: int), *close()
@app.post("/uploadfiles")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}


# REQUEST FORMS AND FILES
# Define file and form fileds at the same time using File() and Form() in the same route - when you need to receive both form fields and files in the same request. They will be uploaded as form data and you will recieve the files and form fields.
@app.post("/files_and_forms")
async def create_file_and_form(
    file: bytes = File(...),
    fileb: UploadFile = File(...),
    token: str = Form(...),
):
    return {
        "file_size": len(file),
        "token": token,
        "fileb_content_type": fileb.content_type,
    }


# HANDLING ERRORS - using HTTPException from FastAPI
error_handling_items = {"foo": "bar"}


@app.get("/error_handling/{item}")
async def get_error_handling(item: str):
    if item not in error_handling_items:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="item not found")
    return {"item": error_handling_items[item]}


# PATH OPERATION DEPENDENCIES (CONFIGURATION)
## params you can pass directly into @decorator (not the function!) to configure the path operation [vs HTTPException which is passed]
## status_code=status.HTTP_###_DETAIL
## tags=['tag_name'] --> pass param a list of str. get added to autogenerated schema documentation to separate endpoints by tagname (can define tag_names in Enum and add that way.)
## summary = '', description='' (description can also be written as markdown and interpreted then displayed in docs formatted)
## response_description='' (note OpenAPI requires path op to have one. If you don't create it defaults to 'Successful response')

# JSON COMPATIBLE ENCODER -jsonable_encoder(object_to_convert_to_JSONcompatible)
## when you need to convert/serialize data type (eg. Pydantic model vales like datetime etc.) to something compatible with JSON (eg. dict, list etc.) for example when you want to store it in a database or for returning JSON responses.
## DOES NOT return a large str with data in JSON format --> retruns standard data structure like a dict that is compatible with JSON --> use json.dumps() to encode to JSON format
### IMP json.dump() can only handle basic Python data types to conevert to JSON format (like lists, dicts, str, nums) while encoder can handle complex data types and change them to JSON compatible data types.


class ConvertToJSON(BaseModel):
    title: str
    timestamp: datetime
    description: Union[str, None] = None


fake_db = {}


@app.put("/convert_to_JSON/{db_item}")
async def update_db_convert_to_json(db_item: str, item: ConvertToJSON):
    json_compatible_item_data = jsonable_encoder(item)
    # converts Pydantic model to a dict and datetime to a str.
    fake_db[item] = json_compatible_item_data
