from fastapi import APIRouter, Depends, HTTPException, Request, Security, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import sqlalchemy
from src import database as db
from sqlalchemy import func
from src import models
from typing import Annotated, Union


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")


async def get_token(request: Request, token: str = Security(oauth2_scheme)):
    if token:
        return token
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Forbidden"
        )


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


class User(BaseModel):
    username: str
    first_name: Union[str, None] = None
    last_name: Union[str, None] = None


def fake_hash_password(password: str):
    return "fakehashed" + password


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


async def get_current_user(token: Annotated[str, Depends(get_token)]):
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


@router.post("/token")
async def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    user = None
    with db.engine.begin() as connection:
        stmt = sqlalchemy.select(
            models.user_table.c.username, models.user_table.c.password)
        stmt = stmt.where(models.user_table.c.username == form_data.username)
        res = connection.execute(stmt)
        user = res.first()

    print(form_data.username)
    if not user:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")
    if not form_data.password == user[1]:
        raise HTTPException(
            status_code=400, detail="Incorrect username or password")

    return {"access_token": user.username, "token_type": "bearer"}


@router.post("/users/create")
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


@router.get("/users/me")
async def read_users_me(
    current_user: Annotated[User, Depends(get_current_active_user)],
):
    return current_user
