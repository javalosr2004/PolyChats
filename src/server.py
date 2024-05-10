from fastapi import FastAPI, exceptions
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import json
import logging
import sys
from src.api import user
from starlette.middleware.cors import CORSMiddleware
from typing import Annotated, Union
from fastapi import APIRouter, Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from src import database as db
import sqlalchemy
from src import models
from src.forms.creation import OAuth2Creation

description = """
Todo...
"""

app = FastAPI(
    title="PolyChats",
    description=description,
    version="0.0.1",
    terms_of_service="http://example.com/terms/",
    contact={
        "name": "Jesus Angel Avalos-Regalado",
        "email": "javalosr@calpoly.edu",
    },
)


app.add_middleware(
    CORSMiddleware,
    allow_methods=["GET", "OPTIONS"],
    allow_headers=["*"],
)

# include routes


@app.exception_handler(exceptions.RequestValidationError)
@app.exception_handler(ValidationError)
async def validation_exception_handler(request, exc):
    logging.error(f"The client sent invalid data!: {exc}")
    exc_json = json.loads(exc.json())
    response = {"message": [], "data": None}
    for error in exc_json:
        response['message'].append(f"{error['loc']}: {error['msg']}")

    return JSONResponse(response, status_code=422)


@app.get("/")
async def root():
    return {"message": "Welcome to [poly]Chats."}


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "fakehashedsecret",
        "disabled": False,
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@example.com",
        "hashed_password": "fakehashedsecret2",
        "disabled": True,
    },
}


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class User(BaseModel):
    username: str
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


def fake_hash_password(password: str):
    return "fakehashed" + password


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


class UserInDB(User):
    password: str


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def fake_decode_token(token):
    # This doesn't provide any security at all
    # Check the next version
    user = None
    with db.engine.begin() as connection:
        res = connection.execute(sqlalchemy.select(
            models.user_table).where(models.user_table.c.username == token))
        user = res.mappings().first()
        if (user):
            user = UserInDB(**user)

    return user


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = fake_decode_token(token)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user


async def get_current_active_user(
    current_user: Annotated[User, Depends(get_current_user)],
):

    return current_user


@app.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = None
    with db.engine.begin() as connection:
        stmt = sqlalchemy.select(
            models.user_table.c.username, models.user_table.c.password)
        stmt = stmt.where(models.user_table.c.username == form_data.username)
        res = connection.execute(stmt)
        user = res.first()

    # user_dict = fake_users_db.get(form_data.username)
    print(form_data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    # user = UserInDB(**user_dict)
    # hashed_password = fake_hash_password(form_data.password)
    if not form_data.password == user[1]:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@app.post("/users/create")
async def create_account(first_name: str, last_name: str, username: str, password: str):
    # check if username is taken.
    user = None
    with db.engine.begin() as connection:
        stmt = sqlalchemy.select(
            sqlalchemy.func.count())
        stmt = stmt.where(models.user_table.c.username == username)
        res = connection.execute(stmt)
        user = res.scalar_one_or_none()
        print(user)
        if (not user):
            # create user with set password
            stmt = sqlalchemy.insert(models.user_table).values({
                "first_name": first_name,
                "last_name": last_name,
                "username": username,
                "password": password
            })
            connection.execute(stmt)
        else:
            raise HTTPException(
                status_code=400, detail="Username already taken. Choose another.")

    return "Account created succesfully!"


@app.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
