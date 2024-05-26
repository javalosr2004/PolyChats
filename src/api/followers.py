from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src import database as db, models
from sqlalchemy import func
from src.api.auth import get_token
from typing import Annotated

router = APIRouter(
    prefix="/followers",
    tags=["followers"],
    dependencies=[Depends(get_token)]
)


@router.post("/{username}/follow")
async def follow_user(token: Annotated[str, Depends(get_token)], username: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Follow a user by their username
    with db.engine.begin() as connection:
        users = models.user_table
        followers = models.followers_table

        find_user_stmt = sqlalchemy.select(users.c.id).where(users.c.username == username)
        find_follower_stmt = sqlalchemy.select(users.c.id).where(users.c.username == user)

        try:
            user_id = connection.execute(find_user_stmt).scalar_one_or_none()
            follower_id = connection.execute(find_follower_stmt).scalar_one_or_none()

            if not user_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            if not follower_id:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Follower not found."
                )

            # Check if already following
            check_follow_stmt = sqlalchemy.select(followers).where(
                followers.c.user_id == user_id,
                followers.c.follower_id == follower_id
            )
            follow_exists = connection.execute(check_follow_stmt).first()
            if follow_exists:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Already following this user."
                )

            # Insert follow relationship
            insert_follow_stmt = sqlalchemy.insert(followers).values({
                "user_id": user_id,
                "follower_id": follower_id
            })
            connection.execute(insert_follow_stmt)
            connection.commit()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to follow."
            )

    return {"message": "Followed successfully"}


@router.delete("/{username}/unfollow")
async def unfollow_user(token: Annotated[str, Depends(get_token)], username: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Unfollow a user by their username
    with db.engine.begin() as connection:
        users = models.user_table
        followers = models.followers_table

        find_user_stmt = sqlalchemy.select(users.c.id).where(users.c.username == username)
        find_follower_stmt = sqlalchemy.select(users.c.id).where(users.c.username == user)

        user_id = connection.execute(find_user_stmt).scalar_one_or_none()
        follower_id = connection.execute(find_follower_stmt).scalar_one_or_none()

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        if not follower_id:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Follower not found."
            )

        unfollow_stmt = sqlalchemy.delete(followers).where(
            followers.c.follower_id == follower_id,
            followers.c.user_id == user_id
        )
        unfollow_result = connection.execute(unfollow_stmt)

        if unfollow_result.rowcount == 0:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Not following user."
            )

    return {"message": "Unfollowed successfully"}
