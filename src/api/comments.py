from fastapi import APIRouter, Depends, HTTPException, status
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

router.post("/create")
async def create_comment(token: Annotated[str, Depends(get_token)], post_id: int ,content: str):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    with db.engine.begin() as connection:
        postComment = sqlalchemy.insert(models.comment_table).values({
           "username": user,
           "post_id":  post_id,
           "content": content
        })

        try:
         response = connection.execute(postComment)
         comment_id = response.inserted_primary_key[0]

        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create comment."
            )

    return {"comment_id": comment_id}
