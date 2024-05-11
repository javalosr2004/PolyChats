import sqlalchemy
from src import database

# SQL table for Users
user_table_metadata = sqlalchemy.MetaData()
user_table = sqlalchemy.Table("User", user_table_metadata, autoload_with=database.engine)

# SQL table for Comment
comment_table_metadata = sqlalchemy.MetaData()
comment_table = sqlalchemy.Table("Comments", comment_table_metadata , autoload_with=database.engine)

# SQL table for Posts
posts_table_metadata = sqlalchemy.MetaData()
post_table = sqlalchemy.Table("Posts", posts_table_metadata, autoload_with=database.engine)

# SQL table for Followers
followers_table_metadata = sqlalchemy.MetaData()
followers_table = sqlalchemy.Table("Followers", followers_table_metadata, autoload_with=database.engine)
