from dotenv import find_dotenv, load_dotenv
from os import getenv



class Config:
    load_dotenv(find_dotenv())
    
    SECRET_KEY = getenv('SECRET_KEY')
    SQLALCHEMY_DATABASE_URI = f'mysql://{getenv("MYSQL_USER")}:{getenv("MYSQL_PASS")}@{getenv("MYSQL_HOST")}:{getenv("MYSQL_PORT")}/{getenv("MYSQL_DB")}'
    SQLALCHEMY_TRACK_MODIFICATIONS = False