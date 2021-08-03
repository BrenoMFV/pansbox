import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    DATABASE_URI = os.environ.get('DATABASE_URI', 'sqlite:///:memory:')
    SQL_ECHO = os.environ.get('SQL_ECHO')
    SECRET_KEY = os.environ.get('SECRET_KEY')