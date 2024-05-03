import sqlalchemy
from src import database

# SQL table for Users
meta_user = sqlalchemy.MetaData()
user_table = sqlalchemy.Table("User", meta_user, autoload_with=database.engine)
