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
async def view_posts(token: Annotated[str, Depends(get_token)], page: int = 1):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if page < 1:
        page = 1
    # returns the 10 most recent posts
    with db.engine.begin() as connection:

        stmt = sqlalchemy.select(
            sqlalchemy.func.count()).select_from(models.post_table)
        pages_available = connection.execute(stmt).scalar_one() // 10
        print(pages_available)

        if (pages_available - ((page - 1) * 10)) < 0:
            return {"prev": pages_available + 1, "next": "", "posts": []}
        stmt = sqlalchemy.text("""
            SELECT p.post_id, p.date, p.user_id, p.post, 
            COUNT(DISTINCT c.id) AS comments, 
            COUNT(DISTINCT CASE WHEN r.like = true THEN r.id ELSE NULL END) AS likes, 
            COUNT(DISTINCT CASE WHEN r.like = false THEN r.id ELSE NULL END) AS dislikes
            FROM "Posts" p
            LEFT JOIN "Comments" c ON c.post_id = p.post_id
            LEFT JOIN "Reactions" r ON r.post_id = p.post_id
            GROUP BY p.post_id, p.date, p.user_id, p.post
            ORDER BY date DESC
            OFFSET :offset
            LIMIT :limit
            """)
        posts = connection.execute(stmt, {"offset": (page-1)*10, "limit": 10}).mappings().all()
        return {
            "prev": return_previous_page(pages_available, page),
            "next": return_next_page(pages_available, page),
            "posts": posts
        }


@router.get("/{id}")
async def view_post_id(token: Annotated[str, Depends(get_token)], id: int):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    with db.engine.begin() as connection:
        # attempt to find post with given id
        if id >= 0:
            # 
            stmt = sqlalchemy.text("""
                SELECT p.post_id, p.date, p.user_id, p.post, 
                COUNT(DISTINCT c.id) AS comments, 
                COUNT(DISTINCT CASE WHEN r.like = true THEN r.id ELSE NULL END) AS likes, 
                COUNT(DISTINCT CASE WHEN r.like = false THEN r.id ELSE NULL END) AS dislikes
                FROM "Posts" p
                LEFT JOIN "Comments" c ON c.post_id = p.post_id
                LEFT JOIN "Reactions" r ON r.post_id = p.post_id
                WHERE p.post_id = :post_id
                GROUP BY p.post_id, p.date, p.user_id, p.post
                """)
            post = connection.execute(stmt, {"post_id": id}).mappings().one_or_none()
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid request. Id not does exist."
                )
            return post


@ router.post("/create")
async def create_post(token: Annotated[str, Depends(get_token)], post: str):
    username = token
    post_id = None
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
   # Fetch the user_id based on the username
    users = models.user_table
    find_username_stmt = sqlalchemy.select(users.c.id).where(users.c.username == username)

    # Creates a post with associated user id
    with db.engine.begin() as connection:

        user_result = connection.execute(find_username_stmt)
        user_id = user_result.scalar()

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found."
            )

        insert_post_stmt = sqlalchemy.insert(models.post_table).values({
            "user_id": user_id,
            "post": post
        })
        try:
            res = connection.execute(insert_post_stmt)
            post_id = res.inserted_primary_key[0]

        except Exception as E:
            print(E)
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to create post."
            )

    return {"post_id": post_id}


@router.delete("/delete/{post_id}")
async def delete_post(token: Annotated[str, Depends(get_token)], post_id: int):
    user = token

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # retrieve the user_id from the users table using the username
    with db.engine.begin() as connection:
        users = models.user_table
        stmt = sqlalchemy.select(users.c.id).where(users.c.username == user)
        user_result = connection.execute(stmt).fetchone()

        if not user_result:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        user_id = user_result.id

    # retrieve the user_id from the post table for the given post_id
    with db.engine.begin() as connection:
        posts = models.post_table
        stmt = sqlalchemy.select(posts.c.user_id).where(posts.c.post_id == post_id)
        post_result = connection.execute(stmt).fetchone()

        if not post_result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Post not found."
            )

        post_user_id = post_result.user_id

        # check if the user_id matches
        if user_id != post_user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to delete this post."
            )

    # deleting the comments and the post
    with db.engine.begin() as connection:
        comments = models.comment_table
        delete_comments_stmt = sqlalchemy.delete(comments).where(comments.c.post_id == post_id)
        connection.execute(delete_comments_stmt)

        delete_post_stmt = sqlalchemy.delete(posts).where(posts.c.post_id == post_id)
        try:
            result = connection.execute(delete_post_stmt)

            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found."
                )

        except Exception as E:
            print(E)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to delete post"
            )

    return {"message": "Post and associated comments deleted successfully", "post_id": post_id}

@router.patch("/update/{post_id}")
async def update_post(token: Annotated[str, Depends(get_token)], post_id: int, new_post: str):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    posts = models.post_table
    users = models.user_table

    # update the post with associated post id
    with db.engine.begin() as connection:
        # retrieve the user_id from the users table using the username
        user_id_stmt = sqlalchemy.select(users.c.id).where(users.c.username == user)
        try:
            user_id_result = connection.execute(user_id_stmt).fetchone()
            if not user_id_result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )

            user_id = user_id_result[0]

            # check if the post belongs to the user
            post_user_id_stmt = sqlalchemy.select(posts.c.user_id).where(posts.c.post_id == post_id)
            post_user_id_result = connection.execute(post_user_id_stmt).fetchone()
            if not post_user_id_result:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found."
                )

            post_user_id = post_user_id_result[0]

            if user_id != post_user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="You do not have permission to update this post."
                )

            # update the post
            update_stmt = sqlalchemy.update(posts).values(post=new_post, date=func.now()).where(posts.c.post_id == post_id)
            result = connection.execute(update_stmt)
            if result.rowcount == 0:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found."
                )
        except Exception as E:
            print(E)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to update post."
            )

    return {"message": "Post updated successfully", "post_id": post_id}

@router.post("/react/{post_id}")
async def react_to_post(token: Annotated[str, Depends(get_token)], post_id: int, like: bool):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    users = models.user_table
    posts = models.post_table
    reactions = models.reations_table

    with db.engine.begin() as connection:
        try:
            # Verify that there is a post with that post id
            post_verification_stmt = sqlalchemy.select(posts).where(posts.c.post_id == post_id)
            post_result = connection.execute(post_verification_stmt)
            if post_result.rowcount != 1:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Post not found."
                )
            
            # Get user id
            user_id_stmt = sqlalchemy.select(users.c.id).where(users.c.username == user)
            user_id_result = connection.execute(user_id_stmt).fetchone()[0]
            if not user_id_result:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid authentication credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            # Determine if there is already a reaction of another type to the post
            check_stmt = sqlalchemy.select(reactions).where(reactions.c.post_id == post_id, reactions.c.user_id == user_id_result)
            check_result = connection.execute(check_stmt)
            check_reaction = check_result.fetchone()
            if check_result.rowcount == 0:   
                # Add a reaction to the table 
                reaction_stmt = sqlalchemy.insert(reactions).values(like=like, post_id=post_id, user_id=user_id_result)          
            elif check_reaction.like != like:
                # Update the reaction
                reaction_stmt = sqlalchemy.update(reactions).values(like=like).where(reactions.c.post_id == post_id, reactions.c.user_id == user_id_result)
            else:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Like already exists." if like else "Dislike already exists."
                )

            connection.execute(reaction_stmt)
        except Exception as E:
            print(E)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Unable to like post." if like else "Unable to dislike post."
            )
        
    return {"message": "Post liked successfully" if like else "Post disliked successfully", "post_id": post_id}
