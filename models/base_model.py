#!/usr/bin/env python
"""Base model to subclass for"""
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session
from uuid import uuid4

JUSTUS_USER = getenv('JUSTUS_USER', 'test')
JUSTUS_PWD = getenv('JUSTUS_PWD', 'test_pwd')
JUSTUS_HOST = getenv('JUSTUS_HOST', 'localhost')
JUSTUS_DB = getenv('JUSTUS_DB', 'justus')
engine = create_engine(
    'postgresql+psycopg2://{user}:{passwd}@{host}/{dbname}'.format(user=JUSTUS_USER, passwd=JUSTUS_PWD,
                                                                   host=JUSTUS_HOST, dbname=JUSTUS_DB))
Base = declarative_base()
Base.metadata.create_all(engine)
# todo: move to proper position
sess_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(sess_factory)
sess = Session()


class BaseModel:
    """Base class with common models methods"""

    def __init__(self, *args, **kwargs):
        """Set up the uuid."""
        self.id = uuid4()
        self.__dict__.update(kwargs)

    def save(self):
        """Save model object to the database"""
        sess.add(self)
        sess.commit()

    def delete(self):
        """Delete user object from database"""
        sess.delete(self)
        sess.commit()
