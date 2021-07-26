import uuid

from . import Base
from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import UUID


class User(Base):
    __tablename__ = 'users'

    id = Column('id', UUID(), default=uuid.uuid4(), primari_key=True, as_uuid=True, index=True)
    username = Column('username', String(32), unique=True, nullable=False)
    email = Column('email', String(64))
    password_hash = Column('password_hash', String(220), nullable=False)

    @property
    def password(self):
        raise AttributeError("Password is not a readable attribute!")

class Account(Base):
    __tablename__ = 'accounts'

    id = Column('id', UUID(), default=uuid.uuid4(), primari_key=True, as_uuid=True, index=True)
