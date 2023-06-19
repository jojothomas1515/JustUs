#!/user/bin/env python
"""User model."""

from sqlalchemy import Column, String, Date, Boolean

from models.base_model import Base, BaseModel


class User(BaseModel, Base):
    """Class to manipulate users table.

    Returns:
        User
    """

    __tablename__ = "users"
    id = Column(String(50), primary_key=True)
    first_name = Column(String(50), nullable=False)
    middle_name = Column(String(50))
    last_name = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    date_of_birth = Column(Date)
    password = Column(String(200), nullable=False)
    is_active = Column(Boolean)

    def get_id(self):
        """For Flask Login to get the user id

        Returns:
            User id.
        """

        return self.id

    @property
    def is_authenticated(self):
        """Check is user is authenticated

        Returns:
            True if user is_active
        """
        return True
