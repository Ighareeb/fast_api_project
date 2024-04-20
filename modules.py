from fastapi import APIRouter

router = APIRouter()


@router.get("/users", tags=["users"])
async def read_users():
    return [{"username": "ABC"}, {"username": "EFG"}]


@router.get("/users/{user_id}", tags=["users"])
async def read_user(user_id: int):
    return {"user_id": user_id}
