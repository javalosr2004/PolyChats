from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src import database as db, models
from src.models import *
from sqlalchemy import func
from src.api.auth import get_token
from typing import Annotated

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    dependencies=[Depends(get_token)]
)


@router.post("/")
async def create_comment(token: Annotated[str, Depends(get_token)], post_id: int, content: str):
    username = token

    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with db.engine.begin() as connection:
        users = models.user_table

        # Fetch the user_id based on the username
        find_username_stmt = sqlalchemy.select(
            users.c.id).where(users.c.username == username)

        try:
            user_result = connection.execute(find_username_stmt)
            user_id = user_result.scalar()

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            # Insert the comment with the fetched user_id
            new_comment_stmt = sqlalchemy.insert(models.comment_table).values({
                "user_id": user_id,
                "post_id": post_id,
                "content": content
            })

            response = connection.execute(new_comment_stmt)
            comment_id = response.inserted_primary_key[0]

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create comment."
            )

    return {"message": "Comment added successfully", "comment_id": comment_id}


@router.delete("/{comment_id}")
async def delete_comment(token: Annotated[str, Depends(get_token)], comment_id: int):
    username = token
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with db.engine.begin() as connection:
        users = models.user_table

        # Fetch the user_id based on the username
        find_username_stmt = sqlalchemy.select(
            users.c.id).where(users.c.username == username)

        try:
            user_result = connection.execute(find_username_stmt)
            user_id = user_result.scalar()

            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="User not found."
                )

            comments = models.comment_table

            # Delete the comment if authorized
            stmt = sqlalchemy.delete(comments).where(
                comments.c.id == comment_id, comments.c.user_id == user_id)
            result = connection.execute(stmt)

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Comment not found"
                )

            connection.commit()

        except Exception as e:
            print(e)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete comment."
            )

    return {"message": "Comment deleted successfully"}
