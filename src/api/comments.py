from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src import database as db, models
from sqlalchemy import func
from src.api.auth import get_token
from typing import Annotated

router = APIRouter(
    prefix="/comments",
    tags=["comments"],
    dependencies=[Depends(get_token)]
)

@router.post("/create")
async def create_comment(token: Annotated[str, Depends(get_token)], post_id: int, content: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    with db.engine.begin() as connection:
        stmt = sqlalchemy.insert(models.comment_table).values({
           "username": user,
           "post_id":  post_id,
           "content": content
        })

        try:
         response = connection.execute(stmt)
         comment_id = response.inserted_primary_key[0]

        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create comment."
            )
    return {"message": "Comment added successfully ", "comment_id": comment_id}

@router.delete("/delete/{comment_id}")
async def delete_comment(token: Annotated[str, Depends(get_token)], comment_id: int):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    comments = models.comment_table

    # deletes the comment if authorized
    with db.engine.begin() as connection:
        stmt = sqlalchemy.delete(comments).where(comments.c.id == comment_id, comments.c.username == user)
        try:
            result = connection.execute(stmt)
            if result.rowcount == 0:
                raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Comment not found"
            )
        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete comment"
            )

    return {"message": "Comment deleted successfully"}