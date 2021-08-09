import os
import uuid
import bcrypt
import datetime

from db_manager import session_factory, Base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column('username', String(32), unique=True, nullable=False)
    email = Column('email', String(64), nullable=False)
    password_hash = Column(String(220), nullable=False)
    sessions = relationship('UserSession', back_populates='user', cascade="all, delete")
    account = relationship('Account', back_populates='user', cascade="all, delete")

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

    @password.setter
    def password(self, password):
        # must decode to utf8 another time so it won't be
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode('utf8')

    def validate_password(self, password):
        return bcrypt.checkpw(password.encode(), self.password_hash.encode())


class UserSession(Base):
    __tablename__ = 'users_session'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    terminal_pid = Column(String(6), default=str(os.getpid()))
    begin = Column(DateTime, default=datetime.datetime.now())
    end = Column(DateTime, nullable=True)
    user = relationship('User', back_populates='sessions')
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
        return '<{0}: Session Started at {1} in the Terminal: {2}>' \
            .format(self.user_id, self.begin, self.terminal_pid)


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(UUID(as_uuid=True), default=uuid.uuid4, primary_key=True)
    site = Column(String(32), index=True)
    username = Column(String(64), index=True)
    password = Column(String(220), index=True)
    user = relationship("User", back_populates='account')
    user_id = Column(Integer, ForeignKey('users.id'))
