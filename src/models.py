import sqlalchemy
from src import database

metadata = sqlalchemy.MetaData()

# SQL table for Users
user_table = sqlalchemy.Table(
    "User", metadata, autoload_with=database.engine)

# SQL table for Comment
comment_table = sqlalchemy.Table(
    "Comments", metadata, autoload_with=database.engine)

# SQL table for Posts
post_table = sqlalchemy.Table(
    "Posts", metadata, autoload_with=database.engine)

# SQL table for Followers
followers_table = sqlalchemy.Table(
    "Followers", metadata, autoload_with=database.engine)

# SQL table for Likes/Dislikes (Reactions)
reactions_table = sqlalchemy.Table(
    "Reactions", metadata, autoload_with=database.engine)

# SQL table for Profile
profile_table = sqlalchemy.Table(
    "Profile", metadata, autoload_with=database.engine)
