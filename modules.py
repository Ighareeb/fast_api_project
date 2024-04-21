from fastapi import APIRouter

router = APIRouter()


@router.get("/users", tags=["users"])
async def read_users():
    return [{"username": "ABC"}, {"username": "EFG"}]


@router.get("/users/{user_id}", tags=["users"])
async def read_user(user_id: int):
    return {"user_id": user_id}


# In main app you will need to import the routers you want to use then use ,app.include_router(name.router) to include them
# can add metadata in the same way as instantiating main FastAPI app
# eg.app.include_router(
#     admin.router,
#     prefix="/admin",
#     tags=["admin"],
#     dependencies=[Depends(get_token_header)],
#     responses={418: {"description": "I'm a teapot"}},
# )
