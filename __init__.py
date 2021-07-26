import psycopg2
from config import Config
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base


DATABASE_URI = os.environ.get(Config.DATABASE_URI, echo=Config.SQL_ECHO)

engine = create_engine(DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

