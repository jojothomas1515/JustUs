#!/usr/bin/env python
"""Base model to subclass for"""
from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker
from os import getenv

JUSTUS_USER = getenv('JUSTUS_USER', 'test')
JUSTUS_PWD = getenv('JUSTUS_PWD', 'test_pwd')
JUSTUS_HOST = getenv('JUSTUS_HOST', 'localhost')
JUSTUS_DB = getenv('JUSTUS_USER', 'justus')
engine = create_engine(
    'postgresql+psycopg2://{user}:{passwd}@{host}/{dbname}'.format(user=JUSTUS_USER, passwd=JUSTUS_PWD,
                                                                   host=JUSTUS_HOST, dbname=JUSTUS_DB))
Base = declarative_base()
print("hello")
# print(Base.metadata.create_all(engine))
print(engine)
Session = sessionmaker(bind=engine)
sess = Session()
