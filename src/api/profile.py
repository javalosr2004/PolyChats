from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
import sqlalchemy
from src.models import *
from src import database as db, models
from sqlalchemy import func
from src.api.auth import get_token
from typing import Annotated
from datetime import datetime

router = APIRouter(
    prefix="/profile",
    tags=["profile"],
    dependencies=[Depends(get_token)],
)


'''by default, all users get a profile created for them
   via postgres trigger,
   every username is unique, thus allowing for username to be used for the associated id
'''


def parse_user_data_from_username(username: str, visitor: str = None):
    # initializing default values
    id = 0
    user = None
    posts = []
    db_profile = None
    user_profile = {
        "Name": None,
        "About Me": None,
        "Account Created": None,
        "Public": True,
        "Username": None,
        "ID": None,
        "Followers": 0,
        "Following": 0,
        "Top Posts": []
    }
    # get user about me and if public
    with db.engine.begin() as connection:
        # querying for username via id
        res = connection.execute(sqlalchemy.select(
            user_table).where(user_table.c.username == username))
        if not (user := res.mappings().first()):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid username.")

        res = connection.execute(sqlalchemy.select(profile_table).where(
            profile_table.c.owner_id == user['id']))
        db_profile = res.mappings().first()
        if not db_profile:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="For some reason you account is glitched. Don't know how,commits should've rolled back during creation.")

        # check if profile is public
        if not db_profile['public'] and visitor != None and visitor != username:
            # check to see if visitor is in friends list
            friend_stmt = sqlalchemy.select(sqlalchemy.func.count()).join(user_table, user_table.c.username == visitor).where(followers_table.c.user_id == user['id']
                                                                                                                              and user_table.c.id == followers_table.c.follower_id)
            res = connection.execute(friend_stmt).scalar_one_or_none()
            if not res:
                '''maybe a little ambitious we'll see if we get to do friend requests'''
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Sorry. This person has made their account private. Request a follow to see their secrets."
                )

        # parse the data
        user_profile["Name"] = str.title(
            user['first_name'] + " " + user["last_name"])
        user_profile["Username"] = user['username']
        user_profile["About Me"] = db_profile["about_me"]
        user_profile["Public"] = db_profile["public"]
        date = datetime.fromisoformat(str(db_profile["created_at"]))

        user_profile["Account Created"] = date.strftime("%B %d, %Y")
        id = user["id"]

        user_profile["ID"] = id

        top_posts = sqlalchemy.select(
            post_table.c.post_id, post_table.c.post,
            sqlalchemy.func.rank().over(order_by=sqlalchemy.func.count(
                reactions_table.c.like).desc()).label('post_rank')
        ).select_from(
            post_table
        ).outerjoin(
            reactions_table, reactions_table.c.post_id == post_table.c.post_id
        ).where(
            post_table.c.user_id == id
        ).group_by(
            post_table.c.post_id
        ).limit(5)
        res = connection.execute(top_posts)

        # add to profile, limit the full text post
        if (posts := res.mappings().all()):
            for post in posts:
                preview = post['post']
                if len(preview) > 20:
                    preview = preview[:20] + "..."
                user_profile['Top Posts'].append(
                    {"id": post['post_id'], "preview": preview, "rank": post['post_rank']})

        # get followers / following
        followers_stmt = sqlalchemy.select(sqlalchemy.func.count()
                                           ).where(followers_table.c.user_id == id)
        followers = connection.execute(followers_stmt).scalar_one_or_none()
        if followers:
            user_profile["Followers"] = followers

        following_stmt = sqlalchemy.select(sqlalchemy.func.count()
                                           ).where(followers_table.c.follower_id == id)
        following = connection.execute(following_stmt).scalar_one_or_none()
        if following:
            user_profile["Following"] = following

    # get user posts - only ids possibly likes and dislikes?? sorted by popularity
    # get user views, alltime???
    # get total likes / dislikes????
    # get total followers / following
    return user_profile


@router.get("/")
async def get_my_profile(token: Annotated[str, Depends(get_token)]):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"})
    # find user id
    return parse_user_data_from_username(user)

    # parse


@router.get("/{username}")
async def get_person_profile(token: Annotated[str, Depends(get_token)], username: str):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return parse_user_data_from_username(username, user)


@router.patch("/")
async def change_profile(token: Annotated[str, Depends(get_token)], public: bool = None, about_me: str = None):
    user = token
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    profile = {}
    if not public and not about_me:
        raise HTTPException(
            status_code=status.HTTP_418_IM_A_TEAPOT, detail="Bro. What are you doing.")
    if public != None:
        profile['public'] = public
    if about_me != None:
        profile['about_me'] = about_me
    with db.engine.begin() as connection:
        id_stmt = sqlalchemy.select(user_table.c.id).where(
            user_table.c.username == user).scalar_subquery()
        stmt = sqlalchemy.update(profile_table).where(
            id_stmt == profile_table.c.owner_id
        )
        try:
            connection.execute(stmt, profile)
        except Exception as e:
            print(e)
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Failed to update profile. Internal server error.")

    return "Profile has been updated!"
