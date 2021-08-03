import uuid
import bcrypt
import datetime

from .db_manager import Base
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relashionship
from sqlalchemy.dialects.postgresql import UUID

from os import getpid


class User(Base):
    __tablename__ = 'users'

    id = Column('id', UUID(), default=uuid.uuid4(), primari_key=True, as_uuid=True, index=True)
    username = Column('username', String(32), unique=True, nullable=False)
    email = Column('email', String(64), nullable=False)
    password_hash = Column(String(220), nullable=False)
    session = relashionship('UserSession', backref='session', )
    account = relashionship('Account', back_populates='user')


    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.hashpw(password.decode(), bcrypt.gensalt())

    def validate_password(self, password):
        return bcrypt.checkpw(self.password_hash, password.decode())


class UserSession(Base):
    __tablename__ = 'users_session'

    id = Column('id', Integer, primary_key=True)
    terminal_pid = Column(String(6), default=os.getpid())
    begin = Column(DateTime, default=datetime.datetime.now())
    end = Column(DateTime)
    user_id = Column(Integer, ForeignKey('users.id'))


    # @property
    # def session(self):
    #     return self.session_hash
    #
    # @session.setter
    # def session_hash(self):
    #     self.session_hash =
    #
    # def verify_session(self):


    def __repr__(self):
        return '<{0}: Session Started at {1} {2}>'.format(self.user_id, self.begin, self.terminal_pid)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column('id', UUID(), default=uuid.uuid4(), primari_key=True, as_uuid=True, index=True)
    site = Column(String(32), index=True)
    username = Column(String(64), index=True)
    password = Column(String(220), index=True)
    user_id = Column(Integer, ForeignKey('users.user_id'))
    user = relationship("User", back_populates='account')
