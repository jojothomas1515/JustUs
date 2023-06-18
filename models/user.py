#!/user/bin/env python
"""User model."""

from sqlalchemy import Column, String, Date

from base_model import Base, BaseModel


class User(BaseModel, Base):
    """Class to manipulate users table."""

    __tablename__ = "users"
    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    password = Column(String(200), nullable=False)
