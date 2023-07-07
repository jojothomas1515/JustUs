#!/usr/bin/env python

"""For instantiating db sessions."""

from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

JUSTUS_USER = getenv('JUSTUS_USER', 'test')
JUSTUS_PWD = getenv('JUSTUS_PWD', 'test_pwd')
JUSTUS_HOST = getenv('JUSTUS_HOST', 'localhost')
JUSTUS_DB = getenv('JUSTUS_DB', 'justus')
engine = create_engine(
    'postgresql+psycopg2://{user}:{passwd}@{host}/{dbname}'.format(user=JUSTUS_USER, passwd=JUSTUS_PWD,
                                                                   host=JUSTUS_HOST, dbname=JUSTUS_DB))
# todo: move to proper position
sess_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = sess_factory
sess = Session()
