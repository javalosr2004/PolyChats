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


def return_previous_page(line_count: int, cur_page: int):
    # prev_page = "/carts/search/"
    if line_count == 0 or cur_page <= 0:
        return ""
    remaining = ((int(line_count) - ((cur_page) * 5))) // 5
    if remaining < -1:
        new_page = (line_count // 5)
    else:
        new_page = cur_page
    return new_page

    # query = re.sub(r'search_page=\d+', f'search_page={new_page}', query)
    # return prev_page + query


def return_next_page(line_count: int, cur_page: int):
    # prev_page = "/carts/search/"
    remaining = ((int(line_count) - ((cur_page) * 5))) // 5
    if remaining <= 0:
        return ""
    new_page = cur_page + 2
    # if (cur_page == 0):
    # return prev_page + query + "&search_page=" + str(new_page)
    # query = re.sub(r'search_page=\d+', f'search_page={new_page}', query)
    return new_page


@router.get("/")
async def view_posts(token: Annotated[str, Depends(get_token)], id: int = -1, page: int = 1):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if (id >= 0 and page > 1):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid request. Id's do not have pages."
        )
    if page < 1:
        page = 1
    # returns the 10 most recent posts
    with db.engine.begin() as connection:
        # attempt to find post with given id
        if id >= 0:
            stmt = sqlalchemy.select(models.post_table).where(
                models.post_table.c.post_id == id)
            post = connection.execute(stmt).mappings().one_or_none()
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request. Id not does exist."
                )
            return post

        stmt = sqlalchemy.select(
            sqlalchemy.func.count()).select_from(models.post_table)
        pages_available = connection.execute(stmt).scalar_one() // 10
        print(pages_available)

        if (pages_available - ((page - 1) * 10)) < 0:
            return {"prev": pages_available + 1, "next": "", "posts": []}
        stmt = sqlalchemy.select(models.post_table).order_by(
            models.post_table.c.date).offset((page-1) * 10).limit(10)
        posts = connection.execute(stmt).mappings().all()
        return {
            "prev": return_previous_page(pages_available, page),
            "next": return_next_page(pages_available, page),
            "posts": posts
        }


@ router.post("/create")
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


@ router.post("/delete/{post_id}")
async def delete_post(token: Annotated[str, Depends(get_token)], post_id: int):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # delete a post by id
    with db.engine.begin() as connection:
        posts = models.post_table
        stmt = sqlalchemy.delete(posts).where(posts.c.post_id == post_id)
        try:
            result = connection.execute(stmt)

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found."
                )

        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete post"
            )

    return {"message": "Post deleted successfully", "post_id": post_id}
