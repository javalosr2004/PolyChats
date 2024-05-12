from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src import database as db, models
from sqlalchemy import func
from src.api.auth import get_token
from typing import Annotated

router = APIRouter(
    prefix="/follow",
    tags=["follow"],
    dependencies=[Depends(get_token)]
)


@router.post("/{username}")
async def follow_user(token: Annotated[str, Depends(get_token)], username: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # follow a user by their id
    with db.engine.begin() as connection:
        users = models.user_table
        followers = models.followers_table

        find_user_stmt = sqlalchemy.select(
            users).where(users.c.username == username)
        insert_follow_stmt = sqlalchemy.insert(followers).values({
            "username": username,
            "follower": user
        })
        try:
            user_result = connection.execute(find_user_stmt)

            if user_result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            connection.execute(insert_follow_stmt)
        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to follow."
            )
    return {"message": "Followed Succesfully"}


@router.delete("/unfollow/{username}")
async def unfollow_user(token: Annotated[str, Depends(get_token)], username: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # unfollow a user by their id
    with db.engine.begin() as connection:
        users = models.user_table
        followers = models.followers_table

        find_user_stmt = sqlalchemy.select(users).where(users.c.username == username)
        unfollow_stmt = sqlalchemy.delete(followers).where(followers.c.follower == user).where(followers.c.username == username)
        try:
            user_result = connection.execute(find_user_stmt)

            if user_result.rowcount == 0:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
                )

            unfollow_result = connection.execute(unfollow_stmt)

            if unfollow_result.rowcount == 0:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not following user."
                )
        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to unfollow."
            )
    return {"message": "Unfollowed Succesfully"}

