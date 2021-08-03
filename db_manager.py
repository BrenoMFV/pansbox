import psycopg2
from config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine(Config.DATABASE_URI)

if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)

session = Session()

Base = declarative_base()



