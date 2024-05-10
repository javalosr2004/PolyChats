from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src import database as db, models
from sqlalchemy import func
from src.api.auth import get_token
from typing import Annotated

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    dependencies=[Depends(get_token)],
)

@router.post("/create")
async def create_post(token: Annotated[str, Depends(get_token)], post: str):
    user = token
    post_id = None
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # creates a post with associated user id
    with db.engine.begin() as connection:
        stmt = sqlalchemy.insert(models.post_table).values({
            "username": user,
            "post": post
        })
        try:
            res = connection.execute(stmt)
            post_id = res.inserted_primary_key[0]

        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create post."
            )

    return {"post_id": post_id}

@router.post("/delete/{post_id}")
async def delete_post(token: Annotated[str, Depends(get_token)], post_id: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # delete a post by id
    with db.engine.begin() as connection:
        stmt = sqlalchemy.delete(models.post_table).where(models.post_table.id == post_id)
        try:
            connection.execute(stmt)

        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create post."
            )

    return {"message": "Post deleted successfully", "post_id": post_id}
