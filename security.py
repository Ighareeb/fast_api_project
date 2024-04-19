from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel

# scenario: BE API in some domain with DE in another domain/diff path same domain/or on mobile app. Want FE to auth with BE with OAuth2 username + password. Tools provided by FastAPI to handle this.
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "hashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "hashedsecret2",
        "disabled": True,
    },
}

app = FastAPI()


def hash_password(password: str):
    return "hashed" + password


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")


class AuthUser(BaseModel):
    username: str
    email: str | None = None
    full_name: str | None = None
    disabled: bool | None = None


class AuthUserInDB(AuthUser):
    hashed_password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return AuthUserInDB(**user_dict)


# this does not provide any security
def decode_token(token):
    return AuthUser(
        username=token + "decodedtoken",
        email="user123@example.com",
        full_name="John Doe",
        disabled=False,
    )


async def get_current_user(token: str = Depends(oauth_scheme)):
    user = decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(current_user: AuthUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


# token endpoint must return a JSON object with token_type=bearer and access_token: str (the access token - in this case just the username WHICH IS INSECURE!)
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_dict = fake_users_db.get(form_data.username)
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    user = AuthUserInDB(**user_dict)
    hashed_password = hash_password(form_data.password)
    if not hashed_password == user.hashed_password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect username or password",
        )
    return {"access_token": user.username, "token_type": "bearer"}


@app.get("/auth_users")
async def read_auth_users(current_user: AuthUser = Depends(get_current_user)):
    return current_user


# **user_dict means - Pass the keys and values of the user_dict directly as key-value arguments, equivalent to:
# AuthUserInDB(
#     username = user_dict["username"],
#     email = user_dict["email"],
#     full_name = user_dict["full_name"],
#     disabled = user_dict["disabled"],
#     hashed_password = user_dict["hashed_password"],
# )


# tokenUrl param is the URL where client (FE) sends username and password to get a token.  Use a relative URL to simplify usage (in this case './token') eg. if API was located at (https://example.com/api/v1/) --> (https://example.com/api/v1/token)
# This does not create an endpoint/path operation. It just defines/declares where to get token.
# calling oauth_scheme in path operation provides a str assigned to param 'token' of the path operation function.
# FastAPI will check req for Auth header and Bearer, token value and return token as str
# need to install python-multipart since OAuth2 yses form data to send username and password
@app.get("/auth_items")
async def read_auth_items(token: str = Depends(oauth_scheme)):
    return {"token": token}
