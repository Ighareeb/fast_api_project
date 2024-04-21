# Customise several metadata configs in FastAPI app - use as params when creating FastAPI app instance
# Able to set the following fields used in openapi spec and the auto-generated api docs portal:
# (title: str - title of the api)(summary: str - short summary)(description: str - short description; can use Markdown)(version: str - *version of the API/APP not of openapi)(terms_of_service: str - must be a URL, ToS for API)
# (contact: dict - contact info for exposed API) --> {name: str, url: str - must be URL format, email: str - must be email format}
# (license_info: dict - license info for exposed API) --> {name: str REQUIRED, identifier: str - SPDX license expression for API, url: str - must be URL format} *IMP* identifier and url field mutually exclusive i.e. can't use both at the same time
# note --> email and url become hypertext links in docs
# Example

from fastapi import FastAPI

description = """
API helps you do awesome stuff. 🚀

## Items

You can **read items**.

## Users

You will be able to:

* **Create users** (_not implemented_).
* **Read users** (_not implemented_).
"""

app = FastAPI(
    title="My API",
    description=description,
    summary="test to customise metadocs for my api",
    version="0.0.1",
    terms_of_service="https://www.example.com/terms/",
    contact={
        "name": "API support",
        "url": "http://www.example.com/support",
        "email": "support@example.com",
    },
    license_info={
        "name": "Apache 2.0",
        "url": "https://www.apache.org/licenses/LICENSE-2.0.html",
        # can't use identifier and url at the same time
        # 'identifier': 'MIT',
    },
)


@app.get("/items")
async def read_items():
    return [{"name": "Katana"}]


# METADATA FOR TAGS
## use (openapi_tags: [{'name', 'description', 'externalDocs': {'description', 'url'}},{tag2} ]) field to add additional metadata for tags used to group path ops

# *IMP* order of tags defined here is used by docs (not how you order your paths below)
tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    },
    {
        "name": "items",
        "description": "Manage items. So _fancy_ they have their own docs.",
        "externalDocs": {
            "description": "Items external docs",
            "url": "https://fastapi.tiangolo.com/",
        },
    },
]

app2 = FastAPI(openapi_tags=tags_metadata)


# using the tags in path operation to assign path --> will separate/organize in generated docs
@app.get("/users", tags=["users"])
async def get_users():
    return [{"name": "Harry"}, {"name": "Ron"}]


@app.get("/items", tags=["items"])
async def get_items():
    return [{"name": "wand"}, {"name": "flying broom"}]


# OpenAPI URL - default OpenAPI schema served at /openapi.json can be configured to serve to different url --> eg. app = FastAPI(openapi_url='/api/v1/openapi.json') or you can disable schema by setting openapi_url=None <also disables auto-generated docs UI that use it>
# DOCS URLS - able to configure the two doc UIs (/docs or /rdeoc):
## same as above --> able to set url where it is served or disable docs_url, redoc_url
