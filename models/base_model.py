#!/usr/bin/env python
"""Base model to subclass for"""

from uuid import uuid4

from sqlalchemy.orm import declarative_base

from models.db import sess

Base = declarative_base()


# Base.metadata.create_all(engine)


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

    @classmethod
    def get(cls, key: object, value: object):
        """Get a specific users
        Args:
            value: the data for to use as filter
            key: the key to filter with

        Returns:
            User
        """
        return sess.query(cls).filter(eval(f'cls.{key}') == value).first()
    @classmethod
    def all(cls):
        """Get all of the class object in the database"""
        return sess.query(cls).all()
    def to_dict(self):
        """convert the object attributes to a dict excluding the password hash"""
        info: dict = self.__dict__.copy()
        info.pop("_sa_instance_state", None)
        info.pop("password", None)
        return info
    def __str__(self):
        """String representation."""
        info: dict = self.__dict__.copy()
        info.pop("_sa_instance_state")
        return (str(info))