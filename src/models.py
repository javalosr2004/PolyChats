import sqlalchemy
from src import database

# SQL table for Users
metaData = sqlalchemy.MetaData()
user_table = sqlalchemy.Table("User", metaData, autoload_with=database.engine)

# SQL table for Comment
comment_table = sqlalchemy.Table("Comment", metaData, autoload_with=database.engine)

# SQL table for Posts
post_table = sqlalchemy.Table("Posts", metaData, autoload_with=database.engine)

# SQL table for Followers
message_table = sqlalchemy.Table("Followers", metaData, autoload_with=database.engine)
