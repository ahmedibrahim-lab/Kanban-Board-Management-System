import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_key'
    MYSQL_HOST = os.environ.get('MYSQL_HOST') or 'host'
    MYSQL_USER = os.environ.get('MYSQL_USER') or 'user'
    MYSQL_PASSWORD = os.environ.get('MYSQL_PASSWORD') or 'password'
    MYSQL_DB = os.environ.get('MYSQL_DB') or 'kanban_db'