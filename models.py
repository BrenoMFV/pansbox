import os
import uuid
import bcrypt
import psycopg2

from config import Config
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

engine = create_engine(Config.DATABASE_URI)
if not database_exists(engine.url):
    create_database(engine.url)

_SessionFactory = sessionmaker(bind=engine)

Base = declarative_base()


def session_factory():
    Base.metadata.create_all(engine)
    return _SessionFactory()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column('username', String(32), unique=True, nullable=False)
    password_hash = Column(String(220), nullable=False)
    sessions = relationship('Session', back_populates='user', cascade="all, delete")
    accounts = relationship('Account', back_populates='user', cascade="all, delete")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        # must decode to utf8 another time so it won't be
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf8')

    def validate_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


class Session(Base):
    __tablename__ = 'sessions'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    start = Column(DateTime, default=datetime.now())
    end = Column(DateTime)
    user = relationship('User', back_populates='sessions', cascade="all, delete")


class BlockedUsername(Base):
    __tablename__ = 'blocked_usernames'

    id = Column(Integer, primary_key=True)
    username = Column(String(32))
    end_block = Column(DateTime, default=(datetime.now() + timedelta(minutes=5)))


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    url = Column(String(32), index=True)
    username = Column(String(64), index=True)
    password = Column(String(220), index=True)
    user = relationship("User", back_populates='accounts')
    user_id = Column(Integer, ForeignKey('users.id'))
