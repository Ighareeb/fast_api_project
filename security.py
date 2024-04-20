from datetime import datetime, timedelta, timezone
import time
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from passlib.context import CryptContext
from jose import jwt, JWTError


# run (openssl rand -hex 32) to get a str [SECRET_KEY]
SECRET_KEY = "45deb7171d949d8f33358e1c5c2268b01d56f68effb96df951d1198ced8f1c95"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MIN = 30

# scenario: BE API in some domain with DE in another domain/diff path same domain/or on mobile app. Want FE to auth with BE with OAuth2 username + password. Tools provided by FastAPI to handle this.
fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
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


# add middleware function
# Keep in mind that custom proprietary headers can be added using the 'X-' prefix
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    # this will add a header to the response with the time it took to process the request and generate a response
    response.headers["X-Process-Time"] = str(process_time)
    return response


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

# create passlib context (used to hash + verify password using algo with util functions)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_pw, hashed_pw):
    return pwd_context.verify(plain_pw, hashed_pw)


def get_password_hash(password):
    return pwd_context.hash(password)


# def hash_password(password: str):
#     return "hashed" + password


class Token(BaseModel):  # E.
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str | None = None


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


# util function to auth user (using util verify_password); return user (compare stored hashed and after hashing incoming password)
def authenitcate_user(db, username: str, password: str):
    user = get_user(fake_users_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


# util function to generate, return JWT access token (encoded BUT NOT encrypted)
def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


# updated get_current_user function that uses JWT token, decodes + verifies token and returns current user
async def get_current_user(token: str = Depends(oauth_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: Optional[str] = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username or "")
    if user is None:
        raise credentials_exception
    return user


# # this does not provide any security
# def decode_token(token):
#     return AuthUser(
#         username=token + "decodedtoken",
#         email="user123@example.com",
#         full_name="John Doe",
#         disabled=False,
#     )

## without JWT Token and pw hashing
# async def get_current_user(token: str = Depends(oauth_scheme)):
#     user = decode_token(token)
#     if not user:
#         raise HTTPException(
#             status_code=status.HTTP_401_UNAUTHORIZED,
#             detail="Invalid authentication credentials",
#             headers={"WWW-Authenticate": "Bearer"},
#         )
#     return user


async def get_current_active_user(current_user: AuthUser = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
    return current_user


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    user = authenitcate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW_Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MIN)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")


# token endpoint must return a JSON object with token_type=bearer and access_token: str (the access token - in this case just the username WHICH IS INSECURE!)
# @app.post("/token")
# async def login(form_data: OAuth2PasswordRequestForm = Depends()):
#     user_dict = fake_users_db.get(form_data.username)
#     if not user_dict:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect username or password",
#         )
#     user = AuthUserInDB(**user_dict)
#     hashed_password = hash_password(form_data.password)
#     if not hashed_password == user.hashed_password:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="Incorrect username or password",
#         )
#     return {"access_token": user.username, "token_type": "bearer"}


@app.get("/auth_users", response_model=AuthUser)
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
