import uuid
from typing import Type

from cachetools import cached
from sqlalchemy import Column, DateTime, ForeignKey, String, Integer, create_engine, func
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy_utils import EmailType, UUIDType

from config import DNS

Base = declarative_base()

class User(Base):

    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(EmailType, unique=True)
    password = Column(String(60), nullable=False)
    created_at = Column(DateTime, server_default=func.now())


class Token(Base):

    __tablename__ = "token"

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


class Ads(Base):

    __tablename__ = "adc"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False, unique=True)
    description = Column(String(500), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    user = relationship("User", lazy="joined")


@cached({})
def get_engine():
    return create_engine(DNS)


@cached({})
def get_session_maker():
    return sessionmaker(bind=get_engine())


def init_db():
    Base.metadata.create_all(bind=create_engine(DNS))


def close_db():
    get_engine().dispose()


ORM_MODEL_CLS = Type[User] | Type[Token] | Type[Ads]
ORM_MODEL = User | Token | Ads
