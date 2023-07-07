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
